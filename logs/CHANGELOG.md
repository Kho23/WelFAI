# WelfareMatch-AI 수정 로그

---

## [2026-06-12] 버그 수정 및 보안 개선

### 1. 보안 — API 키 하드코딩 제거
- **파일**: `core/api_data.py`
- **문제**: 공공데이터 API 키가 소스코드에 직접 기재되어 GitHub에 노출된 상태였음.
- **수정**: `python-dotenv` 라이브러리를 통해 `.env` 파일에서 `WELFARE_API_KEY` 환경변수로 읽도록 변경.
  - `.env` 파일 생성 (`.gitignore`에 이미 등록되어 있어 커밋 제외됨)
  - 키가 없을 경우 `ValueError`를 발생시켜 명확한 에러 메시지 제공
- **조치 사항**: GitHub에 올라간 키는 공공데이터포털에서 재발급 필요.

---

### 2. 버그 — `export_results` 속성명 오타
- **파일**: `main.py` (line 92)
- **문제**: `hasattr(self, 'match_result_data')`로 존재하지 않는 속성을 검사하여 항상 `False`를 반환, 엑셀 내보내기 기능이 동작하지 않았음.
- **수정**: `match_result_data` → `match_results_data`로 오타 수정.

---

### 3. 버그 — `matched_summary` / `matched_url` 미초기화
- **파일**: `threads/match_thread.py` (line 20)
- **문제**: 서비스 목록에서 매칭되는 항목이 하나도 없을 경우, `matched_summary`와 `matched_url` 변수가 초기화되지 않아 `UnboundLocalError` 발생 가능.
- **수정**: `for user in users` 루프 시작 시점에 두 변수를 기본값(`''`, `'URL 없음'`)으로 초기화.

---

### 4. 버그 — AI 매칭 버튼 중복 클릭 방지 누락
- **파일**: `main.py` (line 71)
- **문제**: `run_ai_matching()` 실행 시 `btn_match.setEnabled(True)`로 버튼이 활성화된 채 유지되어, 매칭 스레드 실행 중에도 버튼을 반복 클릭 가능했음.
- **수정**: 매칭 시작 시 `btn_match.setEnabled(False)`로 변경. 매칭 완료 후 `display_matching_results()`에서 다시 `True`로 복원되는 기존 로직 유지.

---

### 5. 개선 — DB 연결 컨텍스트 매니저 적용
- **파일**: `database/db_handler.py`
- **문제**: 모든 함수에서 `conn = get_connection()` → `conn.commit()` → `conn.close()`를 수동으로 관리하여 예외 발생 시 연결이 닫히지 않을 위험이 있었음.
- **수정**: `get_connection()`을 `@contextmanager` 기반으로 재구현.
  - `with self.get_connection() as conn:` 패턴으로 모든 쿼리 함수 통일
  - 예외 발생 시 자동 `rollback`, 정상 종료 시 자동 `commit` 후 `close`

---

from PyQt5.QtCore import QThread, pyqtSignal

class MatchThread(QThread):
    # 매칭 후 결과 리스트를 메인에 던져줄 신호
    finished_signal = pyqtSignal(list)

    def __init__(self, db_handler):
        super().__init__()
        self.db = db_handler

    def run(self):
        """키워드 기반 매칭엔징 구동"""
        # DB에서 모든 대상자, 복지서비스 목록 가져오기
        users = self.db.select_all_users()
        services = self.db.select_all_services()

        match_results = []

        for user in users:
            matched_service_name = '추천 서비스 없음'
            user_keyword = user.disability_type.replace('장애', '') if user.disability_type else ''
        # 서비스 목록을 돌면서 키워드 검사
            for service in services:
                summary = service.summary or ''
                s_name = service.name or ''
                s_url = service.service_url or 'URL 없음'

                if user_keyword and (user_keyword in summary or user_keyword in s_name):
                    matched_service_name = f'[특화] {s_name}'
                    matched_summary = summary
                    matched_url = s_url
                    break
                elif '장애인' in summary or '장애인' in s_name:
                    matched_service_name = f"[공통] {s_name}"
                    matched_summary = summary
                    matched_url = s_url

            match_results.append((user.name, user.disability_type, matched_service_name, matched_summary, matched_url))

        self.finished_signal.emit(match_results)

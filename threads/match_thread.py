from PyQt5.QtCore import QThread, pyqtSignal
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TOP_N = 3  # 사용자당 추천 서비스 개수


class MatchThread(QThread):
    finished_signal = pyqtSignal(list)

    def __init__(self, db_handler):
        super().__init__()
        self.db = db_handler

    def run(self):
        """TF-IDF 코사인 유사도 기반 매칭 엔진"""
        users = self.db.select_all_users()
        services = self.db.select_all_services()

        if not services:
            self.finished_signal.emit([])
            return

        # ① 서비스 문서 생성 — 서비스명 + 요약을 하나의 텍스트로 합침
        #    (서비스명에 중요한 키워드가 많아 두 번 넣어 가중치 높임)
        service_docs = [
            f"{s.name} {s.name} {s.summary}"
            for s in services
        ]

        # ② TF-IDF 벡터라이저 학습 — 서비스 문서 전체를 기준으로 단어 가중치 계산
        vectorizer = TfidfVectorizer()
        service_matrix = vectorizer.fit_transform(service_docs)

        match_results = []

        for user in users:
            # ③ 사용자 프로필을 검색 쿼리 텍스트로 변환
            user_query = ' '.join(filter(None, [
                user.disability_type,
                user.disability_level,
                user.address,
            ]))

            if not user_query.strip():
                match_results.append((
                    user.name, user.disability_type or '정보 없음',
                    '추천 서비스 없음', '', 'URL 없음'
                ))
                continue

            # ④ 사용자 쿼리를 같은 벡터 공간으로 변환
            user_vector = vectorizer.transform([user_query])

            # ⑤ 사용자 벡터 vs 서비스 전체 → 코사인 유사도 계산
            scores = cosine_similarity(user_vector, service_matrix)[0]

            # ⑥ 유사도 높은 순으로 Top N 추출
            top_indices = scores.argsort()[::-1][:TOP_N]

            for rank, idx in enumerate(top_indices):
                service = services[idx]
                score = scores[idx]

                if score < 0.01:
                    # 유사도가 너무 낮으면 의미 없는 추천이므로 스킵
                    label = '추천 서비스 없음'
                    summary = ''
                    url = 'URL 없음'
                else:
                    label = f"[Top{rank + 1}] {service.name}  (유사도: {score:.2f})"
                    summary = service.summary or ''
                    url = service.service_url or 'URL 없음'

                match_results.append((
                    user.name,
                    user.disability_type or '정보 없음',
                    label,
                    summary,
                    url,
                ))

        self.finished_signal.emit(match_results)

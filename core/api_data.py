class api_data:
    """api 관련 설정 정보 (Enum 대신 일반 클래스 사용)"""
    url = 'https://apis.data.go.kr/B554287/NationalWelfareInformationsV001/NationalWelfarelistV001'
    # 🚨 주의: 아래 키 값이 정확한지 확인하세요. 캡처본의 bdd... 로 시작하는 인코딩 키여야 합니다.
    my_api_key = 'bdd207fb7fa5921944f02a1affe6b65eeae605f401a5a64d5598a334616f82a8'

    @classmethod
    def get_request_url(cls):
        return f"{cls.url}?serviceKey={cls.my_api_key}&callTp=L&pageNo=1&numOfRows=100&srchKeyCode=001"
import os
from dotenv import load_dotenv

load_dotenv()

class api_data:
    """api 관련 설정 정보 (Enum 대신 일반 클래스 사용)"""
    url = 'https://apis.data.go.kr/B554287/NationalWelfareInformationsV001/NationalWelfarelistV001'
    my_api_key = os.getenv('WELFARE_API_KEY', '')

    @classmethod
    def get_request_url(cls):
        if not cls.my_api_key:
            raise ValueError('.env 파일에 WELFARE_API_KEY가 설정되지 않았습니다.')
        return f"{cls.url}?serviceKey={cls.my_api_key}&callTp=L&pageNo=1&numOfRows=100&srchKeyCode=001"
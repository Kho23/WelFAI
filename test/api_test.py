import requests

# 1. 🚨 Base URL 뒤에 목록조회 엔드포인트(/NationalWelfarelistV001)를 반드시 붙여야 합니다!
url = 'https://apis.data.go.kr/B554287/NationalWelfareInformationsV001/NationalWelfarelistV001'

my_api_key = 'bdd207fb7fa5921944f02a1affe6b65eeae605f401a5a64d5598a334616f82a8'

# 2. V001 버전에서는 귀찮은 callTp가 빠졌습니다. 페이지 번호와 데이터 개수만 깔끔하게 보냅니다.

# 기존 코드
# request_url = f"{url}?serviceKey={my_api_key}&pageNo=1&numOfRows=10"

# ✅ 수정된 코드 (마지막 필수 파라미터 srchKeyCode=001 추가!)
request_url = f"{url}?serviceKey={my_api_key}&callTp=L&pageNo=1&numOfRows=10&srchKeyCode=001"

print("API 요청 보내는 중... (최신 버전 V001 출동!)")

response = requests.get(request_url)

print(f"상태 코드: {response.status_code}")
print("-" * 50)
print(response.text)
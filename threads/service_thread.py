import requests
import xmltodict

from core.models import WelfareService
from PyQt5.QtCore import QThread, pyqtSignal
from database.db_handler import DB_handler
from core.api_data import api_data

class ServiceImportThread(QThread):
    progress_signal = pyqtSignal(int) # 진행률
    finished_signal = pyqtSignal(bool, str) # 성공여부 / 메세지

    def __init__(self):
        super().__init__()
        self.db = DB_handler()

    def run(self):
        try:
            self.progress_signal.emit(10)
            req_url = api_data.get_request_url()
            res = requests.get(req_url)

            if res.status_code != 200:
                raise Exception(f'API 통신 실패(실패코드:{res.status_code}')
            self.progress_signal.emit(50)

            dict_data = xmltodict.parse(res.text)

            # API 응답 유효성 검사
            if 'wantedList' not in dict_data or 'servList' not in dict_data['wantedList']:
                raise Exception("조회된 복지 서비스 데이터가 없습니다.")

            service_list = dict_data['wantedList']['servList']
            if not isinstance(service_list, list):
                service_list = [service_list]

            self.progress_signal.emit(70)

            data_list = []

            for item in service_list:
                service = WelfareService(
                    name=item.get('servNm', ''),  # 서비스명
                    department=item.get('jurMnofNm', ''),  # 소관부처명
                    summary=item.get('servDgst', ''),  # 서비스 요약
                    target=item.get('trgterIndvdlArray', ''),  # 대상자(가구유형)
                    service_url=item.get('servDtlLink', '')  # 상세 링크
                )
                data_list.append(service)
            self.db.insert_services(data_list)
            self.progress_signal.emit(100)
            self.finished_signal.emit(True, f'총 {len(data_list)} 건의 최신 데이터를 API로 갱신했습니다.')
        except Exception as e :
            print(f' 서비스 임포트 스레드 에러 {e}')
            self.finished_signal.emit(False, f'에러 발생: {str(e)}')
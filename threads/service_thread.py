from zoneinfo import available_timezones

import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
from database.db_handler import DB_handler

class ServiceImportThread(QThread):
    progress_signal = pyqtSignal(int) # 진행률
    finished_signal = pyqtSignal(bool, str) # 성공여부 / 메세지

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.db = DB_handler()

    def run(self):
        try:
            df = pd.read_excel(self.file_path, engine='openpyxl')
            self.progress_signal.emit(30)
            target_col = ['서비스아이디', '서비스명', '서비스URL', '서비스요약', '소관부처명']

            available_col = [col for col in target_col if col in df.columns]

            if len(available_col) < len(target_col):
                missing = set(target_col) - set(available_col)
                raise Exception(f"엑셀 파일 컬럼 부족 오류: {missing}")
            selected_df = df[target_col]

            selected_df = selected_df.fillna("")
            data_list = selected_df.values.tolist()

            self.progress_signal.emit(60)

            if hasattr(self.db, 'insert_services'):
                self.db.insert_services(data_list)
            else:
                self.progress_signal.emit(100)
                self.finished_signal.emit(True, f"총 {len(data_list)} 건의 복지서비스 엑셀 데이터가 업데이트 되었습니다.")

        except Exception as e :
            self.finished_signal.emit(False, f'엑셀 로드 중 오류발생: {str(e)}' )
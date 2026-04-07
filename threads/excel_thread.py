from PyQt5.QtCore import QThread, pyqtSignal
from utils.excel_loader import load_excel
from database.db_handler import DB_handler

class ExcelThread(QThread):
    progress_signal = pyqtSignal(int) # 진행률
    finished_signal = pyqtSignal(bool, str) # 성공여부와 메세지

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.db = DB_handler()

    def run(self):
        """스레드 시작 시 실행되는 함수"""
        try:
            data = load_excel(self.file_path)
            if data:
                total = len(data)
                for i, row in enumerate(data):
                    self.db.insert_user(row[0], row[1], row[2], row[3], row[4])
                    progress = int(((i + 1) / total) * 100)
                    self.progress_signal.emit(progress)
                self.finished_signal.emit(True, f"{total}명의 데이터 조회가 완료되었습니다.")
            else:
                self.finished_signal.emit(False, "엑셀 데이터 형태가 잘못되었거나 비어있습니다.")
        except Exception as e:
            self.finished_signal.emit(False, f"오류 발생: {str(e)}")
            print(f"ExcelThread run exception {e}")

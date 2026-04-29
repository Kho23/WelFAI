import sys
import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5 import uic

from database.db_handler import DB_handler
from threads.excel_thread import ExcelThread
from threads.service_thread import ServiceImportThread
from threads.match_thread import MatchThread
from utils.excel_exporter import export_to_excel

BASE_DIR = os.path.dirname(__file__)
UI_PATH = os.path.join(os.path.dirname(__file__), 'ui', 'main_ui.ui')
OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'output') # 아웃풋 폴더 경로 추가

class WelfareApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DB_handler()
        try:
            uic.loadUi(UI_PATH, self)
        except FileNotFoundError:
            QMessageBox.critical(self, 'ui 파일 로드 실패', f'{UI_PATH} 경로의 파일을 찾을 수 없습니다.')
            sys.exit()
        self.initUI()

    def initUI(self):
        self.btn_import.clicked.connect(lambda : self.open_file_dialog('user'))
        self.btn_service_import.clicked.connect(lambda:self.open_file_dialog('service'))
        self.btn_match.clicked.connect(self.run_ai_matching)
        self.tableWidget.cellDoubleClicked.connect(self.show_service_details)

        self.match_results_data = []

        self.pbar.setValue(0)
        self.label_status.setText('엑셀 파일을 선택해주세요.')

        header = self.tableWidget.horizontalHeader()
        if header:
            header.setSectionResizeMode(2, header.Stretch)

    def open_file_dialog(self, mode):
        """mode 에 따라 실행"""
        if mode == 'user':
            title, file_filter = '대상자 엑셀 선택', 'Excel Files (*.xlsx *.xls)'
            file_path, _ = QFileDialog.getOpenFileName(self, title, '', file_filter)
            if file_path:
                self.run_import_thread(file_path)
        else:
            # 🚨 복지 서비스는 파일을 선택하지 않고 바로 API 호출 쓰레드 실행!
            self.run_service_import_thread()

    def run_import_thread(self, file_path):
        """복지서비스 API 등록 쓰레드 실행"""
        self.btn_service_import.setEnabled(False)
        self.label_status.setText('엑셀 데이터를 읽어오는 중...')

        self.excel_worker = ExcelThread(file_path)
        self.excel_worker.progress_signal.connect(self.pbar.setValue)
        self.excel_worker.finished_signal.connect(self.on_finished)
        self.excel_worker.start()

    def run_service_import_thread(self):
        """복지서비스 API 등록 쓰레드 실행"""
        self.btn_service_import.setEnabled(False)
        self.label_status.setText('공공데이터 API로부터 최신 정보를 가져오는 중...')

        self.service_worker = ServiceImportThread() # 🚨 인자 전달 없음
        self.service_worker.progress_signal.connect(self.pbar.setValue)
        self.service_worker.finished_signal.connect(self.on_finished)
        self.service_worker.start()

    def on_finished(self, success, msg):
        self.btn_import.setEnabled(True)
        self.btn_service_import.setEnabled(True)

        if success:
            self.label_status.setText('등록 완료')
            QMessageBox.information(self, '등록 완료', msg)
        else:
            self.label_status.setText('등록 실패')
            QMessageBox.critical(self, '등록 실패', msg)

    def run_ai_matching(self):
        """AI 자동 매칭 실행 및 테이블 출력"""
        self.label_status.setText('AI 매칭엔진 가동 중')
        self.btn_match.setEnabled(True)
        self.pbar.setValue(10)
        """DB에 저장된 '대상자' 와 '서비스'를 연결해주는 쓰레드 실행"""
        self.match_worker = MatchThread(self.db)
        self.match_worker.finished_signal.connect(self.display_matching_results)
        self.match_worker.start()

    def display_matching_results(self, results):
        """매칭 결과를 테이블에 출력"""
        self.tableWidget.setRowCount(0)
        self.mathched_result_data = results

        for row, data in enumerate(results):
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(data[0])))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(data[1])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(data[2])))

        self.pbar.setValue(100)
        self.btn_match.setEnabled(True)
        self.label_status.setText('매칭이 완료되었습니다.')
        QMessageBox.information(self, '매칭 완료', f'총 {len(results)}건이 매칭되었습니다.')

    def show_service_details(self, row, col):
        """테이블 더블 클릭 시 서비스 상세 정보 팝업 출력"""
        try:
            data = self.mathched_result_data[row]
            service_name = data[2]
            summary = data[3]
            url = data[4]

            msg = f"<b>서비스명:</b> {service_name}<br><br>" \
                  f"<b>요약 내용:</b><br>{summary}<br><br>" \
                  f"<b>상세 링크:</b> <a href='{url}'>바로가기</a>"

            box = QMessageBox(self)
            box.setWindowTitle('서비스 상세 정보')
            box.setText(msg)
            box.setTextFormat(1)
            box.exec_()

        except IndexError:
            pass

    def export_results(self):
        """매칭 결과를 엑셀로 내보내는 함수"""
        if not hasattr(self, 'match_result_data') or not self.match_results_data:
            QMessageBox.warning(self, '경고', '내보낼 데이터가 없습니다. 먼저 AI 매칭을 실행해주세요.')
            return
        self.label_status.setText('엑셀 파일로 저장하는 중...')
        saved_path = export_to_excel(self.match_results_data, OUTPUT_PATH)

        if saved_path:
            self.label_status.setText('엑셀 저장 완료')
            QMessageBox.information(self, '저장 완료', f'결과가 다음 경로에 저장되었습니다. {saved_path}')
        else:
            self.label_status.setText('엑셀 저장 실패')
            QMessageBox.critical(self, '저장 실패', '엑셀 파일 저장 중 오류가 발생했습니다. ')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelfareApp()
    window.show()
    sys.exit(app.exec_())

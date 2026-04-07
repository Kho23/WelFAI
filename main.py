import sys
import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5 import uic

from threads.excel_thread import ExcelThread
from threads.service_thread import ServiceImportThread

UI_PATH = os.path.join(os.path.dirname(__file__), 'ui', 'main_ui.ui')

class WelfareApp(QMainWindow):
    def __init__(self):
        super().__init__()
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

        self.pbar.setValue(0)
        self.label_status.setText('엑셀 파일을 선택해주세요.')

        header = self.tableWidget.horizontalHeader()
        if header:
            header.setSectionResizeMode(2, header.Stretch)

    def open_file_dialog(self, mode):
        if mode == 'user':
            title, file_filter = '대상자 엑셀 선택', 'Excel Files (*.xlsx *.xls)'
        else:
            title, file_filter = '복지 서비스 csv 선택', 'Excel Files (*.xlsx *.xls)'
        file_path, _ = QFileDialog.getOpenFileName(self, title, '', file_filter)
        if file_path:
            if mode == 'user':
                self.run_import_thread(file_path)
            else:
                self.run_service_import_thread(file_path)

    def run_import_thread(self, path):
        self.btn_import.setEnabled(False)
        self.label_status.setText('데이터를 등록 중입니다...')
        self.worker = ExcelThread(path)
        self.worker.progress_signal.connect(self.pbar.setValue)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()

    def run_service_import_thread(self, path):
        self.btn_service_import.setEnabled(False)
        self.label_status.setText('복지서비스 데이터 등록 중')

        self.service_worker = ServiceImportThread(path)
        self.service_worker.progress_signal.connect(self.pbar.setValue)
        self.service_worker.finished_signal.connect(self.on_finished)
        self.service_worker.start()

    def on_finished(self, success, msg):
        self.btn_import.setEnabled(False)
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
        self.pbar.setValue(50)

        self.tableWidget.setRowCount(0)

        sample_results = [
            ("김철수", "지체장애(심함)", "장애인 개인예산제 운영"),
            ("이영희", "시각장애(심하지않음)", "(산재근로자)사회심리재활지원")
        ]

        for row, (name, t, service) in enumerate(sample_results):
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(name))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(t))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(service))
        self.pbar.setValue(100)
        self.label_status.setText('매칭이 완료되었습니다.')
        QMessageBox.information(self, '매칭 완료', 'AI 매칭 엔진이 서비스를 정리했습니다.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelfareApp()
    window.show()
    sys.exit(app.exec_())

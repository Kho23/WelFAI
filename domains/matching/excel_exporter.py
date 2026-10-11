import pandas as pd
import os
from datetime import datetime

def export_to_excel(match_results, output_dir):
    """
    매칭 결과를 엑셀 파일로 저정합니다
    :param match_results: (이름, 장애유형, 서비스명, 요약, URL) 형태의 데이터 리스트
    :param output_dir: 저장할 output 경로
    :return: 성공 시 저장된 파일의 전체 경로, 실패 시 None
    """
    try:
        columns = ['이름', '장애유형', '서비스명', '요약', 'URL']
        df = pd.DataFrame(match_results, columns=columns)
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"매칭결과_{current_time}.xlsx"

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        file_path = os.path.join(output_dir, file_name)

        df.to_excel(file_path, index=False, engine='openpyxl')

        return file_path
    except Exception as e :
        print(f"엑셀 저장 중 오류 발생 : {e}")
        return None
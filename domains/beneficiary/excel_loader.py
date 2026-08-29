import pandas as pd

def load_excel(file_path):
    """
    엑셀 파일을 열어서 튜플 묶음 리스트로 반환
    성함 생년월일 장애유형 장애단계 거주지 순으로 반환
    :param file_path:
    :return:
    """
    try:
        df =pd.read_excel(file_path)
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime('%Y-%m-%d')
        data_list = df.fillna('').values.tolist()
        return data_list
    except Exception as e :
        print(f"def load_excel except {e}")
        return None
import sqlite3
import os

from core.models import UserInfo, WelfareService
from core.enums import DisabilityLevel, DisabilityType

class DB_handler:
    def __init__(self):
        # DB 파일 경로 설정 (현재 파일 기준)
        self.db_path = os.path.join(os.path.dirname(__file__), 'welfare.db')
        self.create_table()

    def get_connection(self):
        """데이터베이스 연결 객체를 반환하는 함수"""
        return sqlite3.connect(self.db_path)

    def create_table(self):
        """프로그램 실행 시 필요한 테이블(Users, Services)이 없으면 생성합니다."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 1. 대상자 정보 테이블 (Users)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birth TEXT,
                disability_type TEXT,
                disability_level TEXT,
                area TEXT,
                reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. 복지 서비스 정보 테이블 (Services)
        # 보내주신 엑셀 파일 컬럼: 서비스아이디, 서비스명, 서비스URL, 서비스요약, 소관부처명
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_id TEXT,
                service_name TEXT,
                service_url TEXT,
                summary TEXT,
                department TEXT
            )
        """)

        conn.commit()
        conn.close()

    # --- 대상자(User) 관련 함수 ---

    def insert_user(self, name, birth, dis_type, dis_level, area):
        """DB에 사용자 정보를 저장합니다."""
        conn = self.get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO Users (name, birth, disability_type, disability_level, area)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (name, birth, dis_type, dis_level, area))
        conn.commit()
        conn.close()

    def select_all_users(self) -> list[UserInfo]:
        """DB에 저장되어 있는 모든 사용자 정보를 불러온 뒤 @dataclass 리스트 형태로 반환합니다."""
        conn = self.get_connection()
        cursor = conn.cursor()
        # id(0), name(1), birth(2), disability_type(3), disability_level(4), area(5), reg_date(6)
        cursor.execute('SELECT id, name, birth, disability_type, disability_level, area FROM Users')
        rows = cursor.fetchall()
        conn.close()

        # 모델 구조(name, birth, disability_type, address, id)에 맞춰 인덱스 배정
        return [UserInfo(
            name=u[1],
            birth=u[2],
            disability_type=u[3],
            disability_level=u[4],
            address=u[5],
            id=u[0]
        ) for u in rows]

    # --- 서비스(Service) 관련 함수 ---

    def insert_services(self, data_list : list[WelfareService]):
        """복지 서비스 데이터 리스트(튜플 묶음)를 통째로 저장합니다."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 기존 데이터를 유지할지, 새로 갱신할지에 따라 DELETE 문을 추가할 수 있습니다.
        # 여기서는 중복 방지를 위해 테이블을 비우고 새로 넣는 방식을 예시로 듭니다.
        cursor.execute("DELETE FROM Services")

        sql = """
              INSERT INTO Services (service_name, service_url, summary, department, service_id)
              VALUES (?, ?, ?, ?, ?)
              """
        params = [(s.name, s.service_url, s.summary, s.department, s.target) for s in data_list]
        cursor.executemany(sql, params)
        conn.commit()
        conn.close()

    def select_all_services(self) -> list[WelfareService]:
        """DB의 모든 복지 서비스를 WelfareService 객체 리스트로 반환합니다."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT service_id, service_name, service_url, summary, department, id FROM Services')
            rows = cursor.fetchall()
            conn.close()

            return [WelfareService(name=s[1],
                service_url=s[2],
                summary=s[3],
                department=s[4],
                target=s[0], # API의 servId를 target 필드에 매핑
                id=s[5])
                    for s in rows]
        except Exception as e:
            print(f'서비스 조회 실패: {e}')
            if conn: conn.close()
            return []

if __name__ == '__main__':
    db = DB_handler()
    # 테스트 데이터 삽입
    db.insert_user("홍길동", "1990-01-01", "지체장애", "심한 장애", "서울시 강남구")
    print("사용자 데이터 삽입 완료")

    users = db.select_all_users()
    print(f"현재 등록된 사용자 수: {len(users)}명")
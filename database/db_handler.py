import sqlite3
import os
from contextlib import contextmanager

from core.models import UserInfo, WelfareService
from core.enums import DisabilityLevel, DisabilityType

class DB_handler:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'welfare.db')
        self.create_table()

    @contextmanager
    def get_connection(self):
        """컨텍스트 매니저 방식의 DB 연결 — with 블록 종료 시 자동으로 commit 후 close"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def create_table(self):
        """프로그램 실행 시 필요한 테이블(Users, Services)이 없으면 생성합니다."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

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

    def insert_user(self, name, birth, dis_type, dis_level, area):
        """DB에 사용자 정보를 저장합니다."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                INSERT INTO Users (name, birth, disability_type, disability_level, area)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (name, birth, dis_type, dis_level, area))

    def select_all_users(self) -> list[UserInfo]:
        """DB에 저장되어 있는 모든 사용자 정보를 UserInfo 리스트로 반환합니다."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, birth, disability_type, disability_level, area FROM Users')
            rows = cursor.fetchall()

        return [UserInfo(
            name=u[1],
            birth=u[2],
            disability_type=u[3],
            disability_level=u[4],
            address=u[5],
            id=u[0]
        ) for u in rows]

    def insert_services(self, data_list: list[WelfareService]):
        """복지 서비스 데이터 리스트를 통째로 저장합니다 (기존 데이터 갱신)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Services")
            sql = """
                INSERT INTO Services (service_name, service_url, summary, department, service_id)
                VALUES (?, ?, ?, ?, ?)
            """
            params = [(s.name, s.service_url, s.summary, s.department, s.target) for s in data_list]
            cursor.executemany(sql, params)

    def select_all_services(self) -> list[WelfareService]:
        """DB의 모든 복지 서비스를 WelfareService 객체 리스트로 반환합니다."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT service_id, service_name, service_url, summary, department, id FROM Services')
                rows = cursor.fetchall()

            return [WelfareService(
                name=s[1],
                service_url=s[2],
                summary=s[3],
                department=s[4],
                target=s[0],
                id=s[5]
            ) for s in rows]
        except Exception as e:
            print(f'서비스 조회 실패: {e}')
            return []

if __name__ == '__main__':
    db = DB_handler()
    db.insert_user("홍길동", "1990-01-01", "지체장애", "심한 장애", "서울시 강남구")
    print("사용자 데이터 삽입 완료")

    users = db.select_all_users()
    print(f"현재 등록된 사용자 수: {len(users)}명")

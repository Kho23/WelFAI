import sqlite3
import os

class DB_handler:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'welfare.db')
        self.create_table()

    def get_connection(self):
        """데이터베이스 연결 객체를 반환하는 함수"""
        return sqlite3.connect(self.db_path)

    def create_table(self):
        """프로그램 실행 시 필요한 테이블이 없으면 신규 생성합니다."""
        conn = self.get_connection()
        cursor = conn.cursor()
        create_query = f"""
        create table if not exists Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birth TEXT,
                disability_type TEXT,
                disability_level TEXT,
                area TEXT,
                reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_query)
        conn.commit()
        conn.close()

    def insert_user(self, name, birth, dis_type, dis_level, area ):
        conn = self.get_connection()
        cursor = conn.cursor()
        sql = f"""
            INSERT INTO Users (name, birth, disability_type, disability_level, area)
            values(?,?,?,?,?)
            """
        cursor.execute(sql, (name, birth, dis_type, dis_level, area ))
        conn.commit()
        conn.close()

    def select_all_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users')
        all_user_info = cursor.fetchall()
        conn.close()
        return all_user_info

if __name__=='__main__':
    db = DB_handler()
    db.insert_user("홍길동", "1990-01-01", "지체장애", "심한 장애", "서울시 강남구")

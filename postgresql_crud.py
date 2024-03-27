# postgresql sample db에서 country table을 이용하여 CRUD를 만들기
# 1. staff table의 모든 데이터를 조회하기
# 2. staff table에 데이터를 추가하기
# 3. staff table의 데이터를 수정하기
# 4. staff table의 데이터를 삭제하기
# class로 만들기

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class StaffCRUD:
    def __init__(self):
        self.conn_params = {
        'dbname': os.getenv("DBNAME"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("PASSWORD"),
        'host': os.getenv("HOST"),  # 데이터베이스 서버가 로컬에 있을 경우
        'port': os.getenv("PORT")
        }
        self.conn = None
        self.connect()
    
    def connect(self):
        """데이터베이스에 연결합니다."""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("데이터베이스에 성공적으로 연결되었습니다.")
        except psycopg2.Error as e:
            print(f"데이터베이스 연결 중 오류가 발생했습니다: {e}")

    def get_next_staff_id(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT MAX(staff_id) FROM staff;")
            max_id = cur.fetchone()[0]
            if max_id is None:
                return 1
            else:
                return max_id + 1
    
    ### staff테이블에 address_id에 not-null 제약조건 위반
    def create_staff(self, first_name,last_name,email):
        """staff 테이블에 새로운 스태프를 추가합니다."""
        staff_id = self.get_next_staff_id()

        print(first_name,last_name)
        with self.conn.cursor() as cur:
            cur.execute("""
            INSERT INTO staff (staff_id,first_name, last_name, email)
            VALUES (%s,%s,%s,%s);
            """, (staff_id,first_name,last_name, email))            
            self.conn.commit()
            print(f'스태프 {first_name} {last_name}이(가) staff {staff_id}로 추가 되었습니다.')
            return staff_id
        
    def read_all_staff(self):
        """staff_id 기반으로 스태프 전체 정보를 조회합니다."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM staff;")
            staffs = cur.fetchall()
            for staff in staffs:
                print(staff)

    def update_staff(self, staff_id, staff):
        with self.conn.cursor() as cur:
            cur.execute("""
            UPDATE staff
            SET staff = %s
            WHERE staff_id = %s;
            """, (staff, staff_id))
            self.conn.commit()
            print(f'스태프 {staff_id}의 정보가 업데이트 되었습니다.')
    
    def delete_staff(self,staff_id):
        """스태프 정보를 삭제합니다."""
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM country WHERE staff_id = %s;", (staff_id,))
            self.conn.commit()
            print(f'staff {staff_id}의 정보가 삭제되었습니다.')
    def close(self):
        self.conn.close()

staff_crud = StaffCRUD()
staff_id = staff_crud.create_staff("박","룡","ryong@gmail.com")


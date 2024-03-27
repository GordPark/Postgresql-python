# 영화 검색 및 추천 시스템 구축
# 영화 검색: 제목, 장르, 배우 등 다양한 조건으로 영화를 검색할 수 있는 기능.
# 추천 시스템: 사용자의 대여 이력이나 선호 장르를 기반 랜덤으로 영화를 추천해주는 기능.
# import psycopg2

# class A: pass

# class B(A): pass

# 상속
# .env : 정보보호

import psycopg2
import os
from dotenv import load_dotenv
import random

load_dotenv()

class FilmCRUD:
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

    def read_film(self, film_id):
        """country_id 기반으로 국가 정보를 전체 조회합니다."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM film;")
            films = cur.fetchone()
            for film in films:
                print(films)

    def update_film(self, film_id, film=None):
        """country 정보를 업데이트합니다."""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE film
                SET film = %s
                WHERE film_id = %s;
            """, (film, film_id))
            self.conn.commit()
            print(f"film {film_id}의 정보가 업데이트되었습니다.")

    def delete_film(self, film_id):
        """영화 정보를 삭제합니다."""
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM film WHERE film_id = %s;", (film_id,))
            self.conn.commit()
            print(f"film {film_id}의 정보가 삭제되었습니다.")
    
    def close(self):    
        self.conn.close()

# film_crud = FilmCRUD()
# film_id = film_crud.create_film("Lion")
# film_crud.read_film(film_id)
# film_crud.update_film(film_id=film_id, country= "Tiger")
# film_crud.delete_film(film_id)

class RecommendedFilm(FilmCRUD):
    def __init__(self):
        super().__init__()
    def search_film(self, title):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM film WHERE title = {title}")
            

    def random_recommended(self, n):
        with self.conn.cursor() as cur:
            cur.execute("SELECT film_id,title FROM film ORDER BY RANDOM() LIMIT %s ",(n,))
            recommended_films = cur.fetchall()
            return recommended_films

test = RecommendedFilm()
user_input = input("추천받을 영화의 개수를 입력하세요.")
print(test.random_recommended(user_input))


    
    
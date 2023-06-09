import psycopg2
from psycopg2 import OperationalError
from config import user_db, password_db

class work_bd():

    @staticmethod
    def connect():
        try:
            connection = None
            # Подключение к существующей базе данных
            connection  = psycopg2.connect(user=user_db,
                                  password=password_db,
                                  host="127.0.0.1",
                                  port="5432",
                                  database="netologyf")
        
            #print("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        return connection


    def create_table():
        try:
            connection = work_bd.connect()
            cursor = connection.cursor()


            cursor.execute("CREATE TABLE IF NOT EXISTS viewed (id SERIAL PRIMARY KEY, profile_id INTEGER, worksheet_id INTEGER)")
            # поддверждаем транзакцию
            connection.commit()
            print("Таблица viewed успешно создана")
 
            cursor.close()
            connection.close()
    
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        return connection


    #добавление в БД
    def to_bd(profile_id, worksheet_id):
        try:
            connection = work_bd.connect()
            cursor = connection.cursor()
        
            view = (profile_id, worksheet_id)
            cursor.execute(f"INSERT INTO viewed (profile_id, worksheet_id) VALUES (%s, %s)", view)

            connection.commit()
            print("Данные в таблицу viewed успешно добавлены")
 
            cursor.close()
            connection.close()

        except OperationalError as e:
            print(f"The error '{e}' occurred")


    #извлечение из БД
    def from_bd(user_id):
        try:
            connection = work_bd.connect()
            cursor = connection.cursor()
            postgresql_select_query = "select worksheet_id from viewed where profile_id = %s"
            cursor.execute(postgresql_select_query, (user_id,))
            mobile_records = cursor.fetchall()
            
            response_from = []
            for row in mobile_records:
                response_from.append(row[0])

            #print(response_from)

            cursor.close()
            connection.close()
            
            return response_from

        except OperationalError as e:
            print(f"The error '{e}' occurred")
        finally:
            response_from

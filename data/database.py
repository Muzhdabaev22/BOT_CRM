import pymysql
from data.logging import logger
from pymysql import cursors


class DatabaseManagerSQL:

    def __init__(self, host, port, user, password, db_name):
        try:
            self.connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=db_name,
                cursorclass=cursors.DictCursor
            )
        except Exception as error:
            logger.error(f"Не удалось подключиться к бд: {error}")

    def query(self, arg, values=None):
        try:
            if values is None:
                with self.connection.cursor() as cur:
                    cur.execute(arg)
            else:
                with self.connection.cursor() as cur:
                    cur.execute(arg, values)
            self.connection.commit()
        except Exception as error:
            logger.error(f"Ошибка с запросом в БД: {error}")

    def fetchone(self, arg, values=None):
        try:
            if values is None:
                with self.connection.cursor() as cur:
                    cur.execute(arg)
                    return cur.fetchone()
            else:
                with self.connection.cursor() as cur:
                    cur.execute(arg, values)
                    return cur.fetchone()
        except Exception as error:
            logger.error(f"Ошибка с запросом(fetchone) из БД: {error}")

    def fetchall(self, arg, values=None):
        try:
            if values is None:
                with self.connection.cursor() as cur:
                    cur.execute(arg)
                    return cur.fetchall()
            else:
                with self.connection.cursor() as cur:
                    cur.execute(arg, values)
                    return cur.fetchall()
        except Exception as error:
            logger.error(f"Ошибка с запросом(fetchone) из БД: {error}")

    def create_tables(self):
        self.query(
            """
            CREATE TABLE IF NOT EXISTS students (
            name VARCHAR(60),
            code VARCHAR(10),
            id_tg VARCHAR(50),
            language VARCHAR(30),
            city VARCHAR(30),
            age TINYINT,
            level VARCHAR(10),
            telephone VARCHAR(30),
            link TEXT,
            goal TEXT,
            form VARCHAR(30),
            dateArrival VARCHAR(15),
            comment TEXT,
            status VARCHAR(30),
            teacher VARCHAR(60),
            PRIMARY KEY(code))
            """)
        self.query("""
            CREATE TABLE IF NOT EXISTS seasonTickets (
            code VARCHAR(10) PRIMARY KEY,
            countLessons TINYINT,
            dateBuy VARCHAR(30),
            classesHeld TEXT,
            FOREIGN KEY(code) REFERENCES students(code))
            """)
        self.query("""
            CREATE TABLE IF NOT EXISTS teachers (
            fullname VARCHAR(60),
            codeLanguage VARCHAR(20),
            tg_id INT,
            PRIMARY KEY(tg_id))
            """)
        self.query("""
            CREATE TABLE IF NOT EXISTS lessonsHistory (
            code VARCHAR(10),
            date DATE,
            lesson_code TEXT)
            """)

    def __del__(self):
        self.connection.close()

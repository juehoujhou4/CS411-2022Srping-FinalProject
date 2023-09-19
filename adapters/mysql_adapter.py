import threading

import pymysql
from queue import Queue


class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.lock = threading.Lock()

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.database,
                charset='utf8mb4',
            )
            print("Connected to database")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")


    # set initial score for selected universities and topic
    def set_initial_score(self, university1, university2, topic):

        university1, university2 = sorted([university1, university2])
        with self.lock:
            try:
                cursor = self.connection.cursor()
                query = f"INSERT INTO scores (university1, university2, topic, score1, score2) VALUES ('{university1}', '{university2}', '{topic}', 0, 0)"
                cursor.execute(query)
                self.connection.commit()
                cursor.close()
            except pymysql.Error as e:
                print(f"Error executing query: {e}. Original query was: {query}")

    # updates the DB with the new score
    def update_score(self, university1, score1, university2, score2, topic):
        m = zip([university1, university2], [score1, score2])
        u1, u2 = sorted(m, key=lambda x: x[0])
        with self.lock:
            try:
                cursor = self.connection.cursor()
                query = f"UPDATE scores SET score1 = {u1[1]}, score2 = {u2[1]} WHERE university1 = '{u1[0]}' AND university2 = '{u2[0]}' AND topic = '{topic}'"
                cursor.execute(query)
                self.connection.commit()
                cursor.close()
            except pymysql.Error as e:
                print(f"Error executing query: {e}. Original query was: {query}")

    def execute_query(self, query):
        with self.lock:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()
                return results
            except pymysql.Error as e:
                print(f"Error executing query: {e}. Original query was: {query}")
                return None

    def execute_query_async(self, query, result_queue: Queue):
        with self.lock:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()
                result_queue.put(results)
            except pymysql.Error as e:
                print(f"Error executing query: {e}. Original query was: {query}")
                result_queue.put(None)



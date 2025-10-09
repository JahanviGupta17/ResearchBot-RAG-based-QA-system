import sqlite3
from datetime import datetime

class QALogger:
    def __init__(self, db_path="qa_history.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS qa_history (
                id INTEGER PRIMARY KEY,
                question TEXT,
                answer TEXT,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def log(self, question: str, answer: str):
        self.conn.execute(
            "INSERT INTO qa_history (question, answer, timestamp) VALUES (?, ?, ?)",
            (question, answer, datetime.now().isoformat())
        )
        self.conn.commit()

    def fetch_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT question, answer, timestamp FROM qa_history ORDER BY id DESC")
        return cursor.fetchall()

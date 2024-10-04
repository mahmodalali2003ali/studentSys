import sqlite3


class Database:
    def __init__(self, db_name="school.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Student (
                            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name TEXT,
                            last_name TEXT,
                            email TEXT,
                            date_of_birth TEXT,
                            date_of_enroll TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Lecturer (
                            lecturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name TEXT,
                            last_name TEXT,
                            email TEXT,
                            hire_date TEXT,
                            department TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Assignment (
                            assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            description TEXT,
                            lecturer_id INTEGER,
                            FOREIGN KEY (lecturer_id) REFERENCES Lecturer (lecturer_id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Grade (
                            grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            grade INTEGER,
                            assignment_id INTEGER,
                            student_id INTEGER,
                            FOREIGN KEY (assignment_id) REFERENCES Assignment (assignment_id),
                            FOREIGN KEY (student_id) REFERENCES Student (student_id))''')

        self.conn.commit()

    def close(self):
        self.conn.close()

from models.database import Database
import sqlite3


class Lecturer:
    def __init__(self, first_name, last_name, email, hire_date, department, lecturer_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hire_date = hire_date
        self.department = department
        self.lecturer_id = lecturer_id


def insert_lecturer(lecturer, db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute('''INSERT INTO Lecturer (first_name, last_name, email, hire_date, department)
                      VALUES (?, ?, ?, ?, ?)''',
                   (lecturer.first_name, lecturer.last_name, lecturer.email, lecturer.hire_date, lecturer.department))
    db_name.conn.commit()


def delete_lecturer(lecturer_id, db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute(
        'DELETE FROM Lecturer WHERE lecturer_id = ?', (lecturer_id,))
    db_name.conn.commit()


def lecturer_exists(lecturer_id, db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute(
        'SELECT COUNT(*) FROM Lecturer WHERE lecturer_id = ?', (lecturer_id,))
    count = cursor.fetchone()[0]
    return count > 0


def update_lecturer(lecturer: Lecturer, db_name: Database):
    if lecturer_exists(lecturer.lecturer_id, db_name):  # تأكد من وجود المحاضر
        cursor = db_name.conn.cursor()
        cursor.execute('''UPDATE Lecturer 
                          SET first_name = ?, last_name = ?, email = ?, hire_date = ?, department = ? 
                          WHERE lecturer_id = ?''',
                       (lecturer.first_name, lecturer.last_name, lecturer.email, lecturer.hire_date, lecturer.department, lecturer.lecturer_id))
        db_name.conn.commit()
        print("Lecturer updated successfully.")
    else:
        print("Lecturer not found.")


def search_lecturer(db_name: Database, name=None, email=None):
    cursor = db_name.conn.cursor()

    if name:
        cursor.execute(
            'SELECT * FROM Lecturer WHERE first_name LIKE ? OR last_name LIKE ?', (f'%{name}%', f'%{name}%'))
    elif email:
        cursor.execute('SELECT * FROM Lecturer WHERE email = ?', (email,))
    else:
        return None  

    return cursor.fetchall()


def fetch_all_lecturers(db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute('SELECT * FROM Lecturer')
    return cursor.fetchall()

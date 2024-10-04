from models.database import Database
import sqlite3


class Assignment:
    def __init__(self, name, description, lecturer_id, assignment_id=None):
        self.name = name
        self.description = description
        self.lecturer_id = lecturer_id
        self.assignment_id = assignment_id


def insert_assignment(assignment, db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute('''INSERT INTO Assignment (name, description, lecturer_id) 
                      VALUES (?, ?, ?)''',
                   (assignment.name, assignment.description, assignment.lecturer_id))

    assignment_id = cursor.lastrowid
    print(f"Inserted assignment with ID: {assignment_id}")

    cursor.execute('SELECT student_id FROM Student')
    students = cursor.fetchall()

    for student in students:
        student_id = student[0]
        cursor.execute('''INSERT INTO Grade (assignment_id, student_id, grade)
                          VALUES (?, ?, ?)''',
                       (assignment_id, student_id, 0))

    db_name.conn.commit()
    print("Inserted grades for all students.")


def delete_assignment(assignment_id, db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute(
        'DELETE FROM Assignment WHERE assignment_id = ?', (assignment_id,))
    db_name.conn.commit()


def assignment_exists(assignment_id, db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute(
        'SELECT COUNT(*) FROM Assignment WHERE assignment_id = ?', (assignment_id,))
    count = cursor.fetchone()[0]
    return count > 0


def update_assignment(assignment: Assignment, db_name: Database):
    if assignment_exists(assignment.assignment_id, db_name): 
        cursor = db_name.conn.cursor()
        cursor.execute('''UPDATE Assignment
                      SET name = ?, description = ?, lecturer_id = ?
                      WHERE assignment_id = ?''',
                       (assignment.name, assignment.description, assignment.lecturer_id, assignment.assignment_id))
        db_name.conn.commit()
        print("Assignment updated successfully.")
    else:
        print("Assignment not found.")


def search_assignment(assignment_id, db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute(
        'SELECT * FROM Assignment WHERE assignment_id = ?', (assignment_id,))
    return cursor.fetchone()


def fetch_all_assignments(db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute('SELECT * FROM Assignment')
    return cursor.fetchall()


def fetch_assignments_by_lecturer(lecturer_id, db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute(
        'SELECT * FROM Assignment WHERE lecturer_id = ?', (lecturer_id,))
    return cursor.fetchall()

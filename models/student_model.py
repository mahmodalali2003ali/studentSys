from models.grade_model import Grade, insert_grade, delete_grade, update_grade, search_grade, fetch_all_grades

from models.database import Database
import sqlite3


class Student:
    def __init__(self, first_name, last_name, email, date_of_birth, date_of_enroll, student_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.date_of_enroll = date_of_enroll
        self.student_id = student_id 



def insert_student(student, db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute('''INSERT INTO Student (first_name, last_name, email, date_of_birth, date_of_enroll) 
                      VALUES (?, ?, ?, ?, ?)''',
                   (student.first_name, student.last_name, student.email, student.date_of_birth, student.date_of_enroll))
    db_name.conn.commit()


def delete_student(student_id, db_name: Database):
    cursor = db_name.conn.cursor()
    # حذف الدرجات المرتبطة بالطالب
    cursor.execute('DELETE FROM Grade WHERE student_id = ?', (student_id,))
    # حذف الطالب
    cursor.execute('DELETE FROM Student WHERE student_id = ?', (student_id,))
    db_name.conn.commit()
    print(f"Deleted student {student_id} and related grades.")


def student_exists(student_id, db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute(
        'SELECT COUNT(*) FROM Student WHERE student_id = ?', (student_id,))
    count = cursor.fetchone()[0]
    return count > 0


def update_student(student: Student, db_name: Database):
    if student_exists(student.student_id, db_name):
        cursor = db_name.conn.cursor()
        cursor.execute('''UPDATE Student 
                          SET first_name = ?, last_name = ?, email = ?, date_of_birth = ?, date_of_enroll = ? 
                          WHERE student_id = ?''',
                       (student.first_name, student.last_name, student.email, student.date_of_birth, student.date_of_enroll, student.student_id))
        db_name.conn.commit()
        print("Student updated successfully.")
    else:
        print("Student not found.")


def search_student(student_id, date_of_birth, db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute('SELECT * FROM Student WHERE student_id = ? AND date_of_birth=?',
                   (student_id, date_of_birth))
    return cursor.fetchone()


def fetch_all_students(db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute('SELECT * FROM Student')
    return cursor.fetchall()


def find_students_by_birthdate(db_name: Database, start_date, end_date):
    cursor = db_name.conn.cursor()
    cursor.execute(
        '''SELECT * FROM Student WHERE date_of_birth BETWEEN ? AND ?''',
        (start_date, end_date)
    )
    students = cursor.fetchall()
    return students


def fetch_student_with_grades(student_id, db_name: Database):
    cursor = db_name.conn.cursor()

    query = '''
    SELECT Student.first_name, Student.last_name, Assignment.name, Grade.grade
    FROM Student
    JOIN Grade ON Student.student_id = Grade.student_id
    JOIN Assignment ON Grade.assignment_id = Assignment.assignment_id
    WHERE Student.student_id = ?
    '''

    cursor.execute(query, (student_id,))
    result = cursor.fetchall()

    if result:
        print(f"Grades for student {result[0][0]} {result[0][1]}:")
        for row in result:
            print(f"Assignment: {row[2]}, Grade: {row[3]}")
    else:
        print("No grades found for this student.")

    return result


def get_students_with_assignment(assignment_id, db_name: Database):
    cursor = db_name.conn.cursor()

    query = '''
    SELECT Student.student_id, Student.first_name, Student.last_name
    FROM Student
    JOIN Grade ON Student.student_id = Grade.student_id
    JOIN Assignment ON Grade.assignment_id = Assignment.assignment_id
    WHERE Assignment.assignment_id = ?
    '''

    cursor.execute(query, (assignment_id,))
    students = cursor.fetchall()

    if students:
        print(f"Students with Assignment ID {assignment_id}:")
        for student in students:
            print(f"ID: {student[0]}, Name: {student[1]} {student[2]}")
    else:
        print("No students found for this assignment.")

    return students

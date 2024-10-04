import time
from models.database import Database
import sqlite3


class Grade:
    def __init__(self, grade, assignment_id, student_id, grade_id=None):
        self.grade = grade
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.grade_id = grade_id


def insert_grade(grade, db_name: Database):
    try:
        cursor = db_name.conn.cursor()
        cursor.execute('''INSERT INTO Grade (grade, assignment_id, student_id) 
                          VALUES (?, ?, ?)''',
                       (grade.grade, grade.assignment_id, grade.student_id))
        db_name.conn.commit()
        print(f"Inserted grade: {grade}")
    except sqlite3.Error as e:
        print(f"Error inserting grade: {e}")


def delete_grade(grade_id, db_name: Database):
    try:
        cursor = db_name.conn.cursor()
        cursor.execute('DELETE FROM Grade WHERE grade_id = ?', (grade_id,))
        db_name.conn.commit()
        print(f"Deleted grade with id: {grade_id}")
    except sqlite3.Error as e:
        print(f"Error deleting grade: {e}")


def grade_exists(grade_id, db_name: Database):
    try:
        cursor = db_name.conn.cursor()
        cursor.execute(
            'SELECT COUNT(*) FROM Grade WHERE grade_id = ?', (grade_id,))
        count = cursor.fetchone()[0]
        return count > 0
    except sqlite3.Error as e:
        print(f"Error checking if grade exists: {e}")
        return False


def update_grade(grade, db_name: Database):
    for attempt in range(5):  
        try:
            with db_name.conn: 
                if not grade_exists(grade.grade_id, db_name):
                    print(f"No grade found with grade_id {grade.grade_id}")
                    return  

                cursor = db_name.conn.cursor()
                cursor.execute(
                    'SELECT * FROM Grade WHERE grade_id = ?', (grade.grade_id,))
                existing_grade = cursor.fetchone()
                print(f"Grade before update: {existing_grade}")

                cursor.execute('''UPDATE Grade 
                                  SET grade = ?, assignment_id = ?, student_id = ? 
                                  WHERE grade_id = ?''',
                               (grade.grade, grade.assignment_id, grade.student_id, grade.grade_id))

               
                cursor.execute(
                    'SELECT * FROM Grade WHERE grade_id = ?', (grade.grade_id,))
                updated_grade = cursor.fetchone()
                print(f"Grade after update: {updated_grade}")
            return 
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                print("Database is locked, retrying...")
                time.sleep(1)  
            else:
                print(f"An error occurred: {e}")
                break  
        except sqlite3.Error as e:
            print(f"Error updating grade: {e}")


def search_grade(grade_id, db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute('SELECT * FROM Grade WHERE grade_id = ?', (grade_id,))
    return cursor.fetchone()


def fetch_all_grades(db_name: Database):
    cursor = db_name.conn.cursor()
    cursor.execute('SELECT * FROM Grade')
    return cursor.fetchall()


def fetch_grades_by_assignment(assignment_id, name, db_name: Database):
    cursor = db_name.conn.cursor()
    print(f"Assignment name : {name}  AssignmentId : {assignment_id}")
    cursor.execute(
        'SELECT * FROM Grade WHERE assignment_id = ?', (assignment_id,))
    return cursor.fetchall()

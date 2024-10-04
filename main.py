from models.database import Database
from models.student_model import Student, insert_student, delete_student, update_student, search_student, fetch_all_students, fetch_student_with_grades, find_students_by_birthdate, get_students_with_assignment
from models.lecturer_model import Lecturer, insert_lecturer, delete_lecturer, update_lecturer, search_lecturer, fetch_all_lecturers
from models.assignment_model import Assignment, insert_assignment, delete_assignment, update_assignment, search_assignment, fetch_all_assignments, fetch_assignments_by_lecturer
from models.grade_model import Grade, insert_grade, delete_grade, update_grade, search_grade, fetch_all_grades, fetch_grades_by_assignment
import sqlite3

def main():
    db = Database()
    try:
        print('----------------------students-----------------------------------------\n')
        #student1 = Student('housam', 'srajali', 'housam@gmail.com','10/10/2003', '10/10/2023'
        #student_to_update = Student('Ahmad', 'Alali', 'mah@gmail.com', '10/10/2002', '10/10/2023', student_id=1)
        #update_student(student_to_update, db)
        #insert_student(student1,db)
        #delete_student(2,db)
        students = fetch_all_students(db)
        for student in students:
            print(student)
        print('\n----------------------Lecturer-----------------------------------------\n')
        lecturer1 = Lecturer("mouhamd", "dbaich",
                             'dbaich@gmail.com', '10/5/2002', 'web developer')
        #lecturerupdate = Lecturer("housam", "dbaich", 'dbaich@gmail.com', '10/5/2003', 'web developer',lecturer_id=1)
        #insert_lecturer(lecturer1,db)
        #delete_lecturer(2,db)
        #update_lecturer(lecturerupdate, db)
        #p= search_lecturer(1,db)
        #print(p)
        lecturers = fetch_all_lecturers(db)
        for lecturer in lecturers:
            print(lecturer)
        print('\n----------------------Assignment-----------------------------------------\n')
        assignment1 = Assignment("html", 'disinge web priviec user ', 1)
        assignment2 = Assignment("css", 'disinge web priviec user ', 2)
        #insert_assignment(assignment1, db)
        #insert_assignment(assignment2, db)
        #delete_assignment(4, db)
        #update_assignment(assignment2, db)
        #search_assignment1=search_assignment(2,db)
        #print(search_assignment1)
        assignments = fetch_all_assignments(db)
        for assignment in assignments:
            print(assignment)
        print('\n----------------------Grade-----------------------------------------\n')
        #grade1 = Grade(100, 1, 2)
        #insert_grade(grade1, db)
        #grad = search_grade(2, db)
        #print(grad)
        #delete_grade(1,db)
        #delete_student(1,db)
        grades = fetch_all_grades(db)
        for grad in grades:
            print(grad)
        print('\n----------------------students----------------------------------------\n')
        get_students_with_assignment(2, db)
        print('\n----------------------Grades for student-------------------------------\n')
        fetch_student_with_grades(1, db)
        print('----------------------students-----------------------------------------')
        # تواريخ البداية والنهاية
        start_date = '01-01-2002'
        end_date = '31-12-2003'
        # استدعاء الدالة
        students_in_range = find_students_by_birthdate(
            db, start_date, end_date)
        print()
        # طباعة النتائج
        for student in students_in_range:
            print(student)
        print('\n----------------------fetch_assignments_by_lecturer--------------------------------\n')
        lst_lect = fetch_assignments_by_lecturer(1, db)
        for lecturer in lst_lect:
            print(lecturer)
        print('\n----------------------fetch_grades_by_assignment-----------------------------------\n')
        lst_assig = fetch_grades_by_assignment(1, 'html', db)
        for assignment in lst_assig:
            print(assignment)
        print('\n-------------------------------------serach---------------------------------------\n')
        # البحث عن طريق الاسم
        lecturers_by_name = search_lecturer(name='mouhamd', db_name=db)
        for lecturer in lecturers_by_name:
            print(lecturer)
        # البحث عن طريق البريد الإلكتروني
        lecturers_by_email = search_lecturer(
            email='example@example.com', db_name=db)
        for lecturer in lecturers_by_email:
            print(lecturer)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close() 
if __name__ == "__main__":
    main()

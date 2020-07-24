from pgDBcm import UseDatabase, ConnectionError, CredentialsError, SQLError

config = {'database': 'students_gpa_db', 'user':'rts',
          'password': 'RVIA2016', 'host': '127.0.0.1', 'port':'5432'}

def create_db(): # создает таблицы
    cursor.execute('''
        create table if not exists Student
        (student_id serial primary key not null,
        name varchar(100) not null, gpa numeric(10,2) null,
        birth timestamp with time zone null);
        
        create table if not exists Course
        (course_id serial primary key not null, name varchar(100) not null);
        ''')

    cursor.execute('''
        create table if not exists Student_Course
        (id serial primary key, student_id integer references Student(student_id),
        course_id integer references Course(course_id));
        ''')

def add_course(course_id, course_name):
    cursor.execute('''
        insert into Course(course_id, name) values(%s, %s);
        ''', (course_id, course_name,))

def get_students(course_id): # возвращает студентов определенного курса
    cursor.execute('''
            select c.name, s.student_id, s.name, s.gpa, s.birth from student_course sc
            join student s on s.student_id = sc.student_id
            join course c on c.course_id = sc.course_id
            where c.course_id = (%s);
        ''', (course_id,))
    return cursor.fetchall()

def add_students(course_id, students): # создает студентов и 
                                       # записывает их на курс
    if course_id:
        for student in students:
            cursor.execute('''
            insert into Student(name, gpa, birth) values(%s, %s, %s) returning student_id;
            ''', (student.get('name'), student.get('gpa'), student.get('birth'),))
            students_id = cursor.fetchone()
            cursor.execute('''insert into Student_Course(student_id, course_id)
                           values(%s, %s);''', (students_id, course_id))
    else:
        print(f'There is not coutseid with № {course_id}')

def add_student(student: dict): # просто создает студента  
    cursor.execute('''
        insert into Student(name, gpa, birth) values(%s, %s, %s);
        ''', (student['name'], student['gpa'], student['birth'],))

def get_student(student_id):   
    cursor.execute('''
        select * from Student where student_id=%s;
        ''', (student_id,))
    return cursor.fetchone()

if __name__ == '__main__':

    students = ({'name': 'Rinat', 'gpa': 8.4, 'birth': '1992.02.11'},
        {'name': 'Oleg', 'gpa': 8.3, 'birth': '1995.07.25'},
        {'name': 'Andrew', 'gpa': 9.1, 'birth': '1993.05.08'},)
   
    with UseDatabase(config) as cursor:
        create_db()
##        add_student({'name': 'Igor', 'gpa': 7.5, 'birth': '11.02.1990'})
##        add_course(1, 'PostgreSQL')
##        add_students(1, students)
        print(get_student(1))
        print(get_students(1))
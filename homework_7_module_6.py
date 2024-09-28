import sqlite3
from faker import Faker
import random
from datetime import datetime

conn = sqlite3.connect('DBhomework')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT NOT NULL
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups(id)
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    grade INTEGER CHECK (grade >= 1 AND grade <= 100),
    grade_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
)''')

fake = Faker()

groups = ['Group A', 'Group B', 'Group C']
for group in groups:
    cur.execute("INSERT INTO groups (group_name) VALUES (?)", (group,))

teachers = []
for _ in range(4):
    first_name = fake.first_name()
    last_name = fake.last_name()
    cur.execute("INSERT INTO teachers (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
    teachers.append(cur.lastrowid)

courses = ['Mathematics', 'Physics', 'History', 'Programming', 'Philosophy']
for course in courses:
    teacher_id = random.choice(teachers)
    cur.execute("INSERT INTO courses (course_name, teacher_id) VALUES (?, ?)", (course, teacher_id))

for _ in range(50):
    first_name = fake.first_name()
    last_name = fake.last_name()
    group_id = random.randint(1, len(groups))
    cur.execute("INSERT INTO students (first_name, last_name, group_id) VALUES (?, ?, ?)", (first_name, last_name, group_id))

cur.execute("SELECT id FROM students")
student_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT id FROM courses")
course_ids = [row[0] for row in cur.fetchall()]

for student_id in student_ids:
    for course_id in course_ids:
        for _ in range(5):
            grade = random.randint(50, 100)
            grade_date = fake.date_between(start_date='-1y', end_date='today')
            cur.execute("INSERT INTO grades (student_id, course_id, grade, grade_date) VALUES (?, ?, ?, ?)", (student_id, course_id, grade, grade_date))

conn.commit()
cur.close()
conn.close()
print("Дані успішно згенеровані")

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Group, Student, Teacher, Subject, Grade
from faker import Faker
import random

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

faker = Faker()

# Генеруємо групи
groups = [Group(name=f"Group {i}") for i in range(1, 4)]
session.add_all(groups)
session.commit()

# Генеруємо викладачів
teachers = [Teacher(name=faker.name()) for _ in range(5)]
session.add_all(teachers)
session.commit()

# Генеруємо предмети
subjects = []
for i in range(1, 9):
    teacher = random.choice(teachers)
    subject = Subject(name=f"Subject {i}", teacher=teacher)
    subjects.append(subject)
session.add_all(subjects)
session.commit()

# Генеруємо студентів
students = [Student(name=faker.name(), group=random.choice(groups)) for _ in range(50)]
session.add_all(students)
session.commit()

# Генеруємо оцінки
grades = []
for student in students:
    for subject in subjects:
        for _ in range(random.randint(1, 20)):
            grade = Grade(
                student=student, 
                subject=subject, 
                teacher=subject.teacher,
                grade=random.uniform(1, 10)
            )
            grades.append(grade)

session.add_all(grades)
session.commit()
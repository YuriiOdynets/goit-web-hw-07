from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, desc, cast, Numeric
from models import Student, Grade, Group, Subject, Teacher

# Підключення до бази даних
engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

# Список селектів із завдання
def select_1():
    """Find 5 students with the highest average grade across all subjects."""
    result = (
        session.query(
            Student.name,
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("average_grade"),
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(5)
        .all()
    )
    return result

def select_2(subject_id: int):
    """Find the student with the highest average grade in a specific subject."""
    result = (
        session.query(
            Student.name,
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("average_grade"),
        )
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .first()
    )
    return result

def select_3(subject_id: int):
    """Find the average grade in groups for a specific subject."""
    result = (
        session.query(
            Group.name,
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("average_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Group, Student.group_id == Group.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.name)
        .all()
    )
    return result

def select_4():
    """Find the average grade across all grades in the database."""
    result = session.query(func.round(cast(func.avg(Grade.grade), Numeric), 2)).scalar()
    return result

def select_5(teacher_id: int):
    """Find the courses taught by a specific teacher."""
    result = session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
    return [row[0] for row in result]

def select_6(group_id: int):
    """Find the list of students in a specific group."""
    result = session.query(Student.name).filter(Student.group_id == group_id).all()
    return [row[0] for row in result]

def select_7(group_id: int, subject_id: int):
    """Find the grades of students in a specific group for a specific subject."""
    result = (
        session.query(Student.name, Grade.grade)
        .select_from(Student)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    return result

def select_8(teacher_id: int):
    """Find the average grade given by a specific teacher across their subjects."""
    result = (
        session.query(
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("average_grade")
        )
        .select_from(Grade)
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )
    return result

def select_9(student_id: int):
    """Find the list of courses attended by a specific student."""
    result = (
        session.query(Subject.name)
        .select_from(Grade)
        .join(Subject)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )
    return [row[0] for row in result]

def select_10(student_id: int, teacher_id: int):
    """Find the list of courses taught to a specific student by a specific teacher."""
    result = (
        session.query(Subject.name)
        .select_from(Grade)
        .join(Subject)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )
    return [row[0] for row in result]

# Виконання запитів та друк результатів
print("Select 1:")
result1 = select_1()
for row in result1:
    print(row)

print("\nSelect 2:")
result2 = select_2(1)
print(result2)

print("\nSelect 3:")
result3 = select_3(1)
for row in result3:
    print(row)

print("\nSelect 4:")
result4 = select_4()
print(result4)

print("\nSelect 5:")
result5 = select_5(5)
print(result5)

print("\nSelect 6:")
result6 = select_6(1)
print(result6)

print("\nSelect 7:")
result7 = select_7(1, 1)
for row in result7:
    print(row)

print("\nSelect 8:")
result8 = select_8(2)
print(result8)

print("\nSelect 9:")
result9 = select_9(5)
print(result9)

print("\nSelect 10:")
result10 = select_10(1, 2)
print(result10)
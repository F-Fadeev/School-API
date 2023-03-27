from random import choice, randint

from sqlalchemy import insert, create_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from db_upload.school_data import first_names, last_names, middle_names, groups, courses
from source.db.database import Base
from source.db.models import Student, Group, Course

engine = create_engine(settings.get_database_url())
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def load_data() -> None:
    s = Session()
    try:
        data = insert(Group).values([{'name': value} for value in groups])
        s.execute(data)
        s.commit()

        data = insert(Student).values([{
            'group_id': randint(1, 10),
            'first_name': choice(first_names),
            'last_name': choice(last_names),
            'middle_name': choice(middle_names),
        } for _ in range(200)])
        s.execute(data)
        s.commit()

        data = insert(Course).values([{'name': value} for value in courses])
        s.execute(data)
        s.commit()

        db_courses = s.query(Course).all()
        db_students = s.query(Student).all()
        for student in db_students:
            student.courses.extend(list({
                db_courses[randint(0, len(db_courses) - 1)] for _ in range(randint(1, 6))
            }))
        s.commit()
    except Exception:
        s.rollback()
    finally:
        s.close()


if __name__ == '__main__':
    load_data()

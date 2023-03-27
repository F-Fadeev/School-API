from sqlalchemy import insert
from sqlalchemy.orm import Session

from source.db.models import Student, Group, Course


def load_test_data(get_session: Session) -> None:
    with get_session as s:
        group = insert(Group).values({'name': 'test'})
        s.execute(group)
        s.commit()

        student = insert(Student).values({
            'group_id': 1,
            'first_name': 'test',
            'last_name': 'test',
            'middle_name': 'test',
        })
        s.execute(student)
        s.commit()

        course = insert(Course).values({'name': 'test', 'description': 'test'})
        s.execute(course)
        s.commit()

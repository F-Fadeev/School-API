from fastapi.testclient import TestClient
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from source.api.schemas.courses_schemas import CourseScheme
from source.db.models import Course, association_table


def test_get_courses(get_client: TestClient, db: Session, get_token: str) -> None:
    client = get_client
    response = client.get(
        '/api/courses',
        headers={'Authorization': f'Bearer {get_token}'},
    )
    query = select(Course)
    result = db.execute(query).scalars().all()
    assert response.status_code == 200
    assert len(response.json()) == len(result)


def test_get_specific_course(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.get(
        '/api/courses/',
        params={'course_id': 1},
        headers={'Authorization': f'Bearer {get_token}'},
    )
    query = select(Course).filter_by(id=1)
    result = db.execute(query).scalars().first()
    assert response.status_code == 200
    assert response.json()[0] == CourseScheme.from_orm(result).dict()


def test_create_course(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.post(
        '/api/courses/create',
        json={'name': 'test2', 'description': 'test2'},
        headers={'Authorization': f'Bearer {get_token}'},
    )
    query = select(Course).filter_by(id=2)
    result = db.execute(query).scalars().first()
    assert response.status_code == 201
    assert response.json() == CourseScheme.from_orm(result).dict()


def test_delete_course(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.delete(
        '/api/courses/delete/1',
        headers={'Authorization': f'Bearer {get_token}'},
    )
    data = select(Course).filter_by(id=1)
    result = db.execute(data).scalars().first()
    assert response.status_code == 204
    assert result is None


def test_update_course(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.put(
        '/api/courses/update/1',
        json={'name': 'test2', 'description': 'test2'},
        headers={'Authorization': f'Bearer {get_token}'},
    )
    query = select(Course).filter_by(id=1)
    result = db.execute(query).scalars().first()
    assert response.status_code == 202
    assert response.json() == CourseScheme.from_orm(result).dict()


def test_enroll_students(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.post(
        '/api/courses/enroll/1',
        json={'student_ids': [1]},
        headers={'Authorization': f'Bearer {get_token}'},
    )
    query = select(association_table).filter(
        association_table.c.course_id == 1,
        association_table.c.students_id == 1,
    )
    result = db.execute(query).one()
    assert response.status_code == 201
    assert result == (1, 1)


def test_expel_students(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    query = insert(association_table).values({'course_id': 1, 'students_id': 1})
    db.execute(query)
    response = client.post(
        '/api/courses/expel/1',
        json={'student_ids': [1]},
        headers={'Authorization': f'Bearer {get_token}'},
    )
    query = select(association_table).filter(
        association_table.c.course_id == 1,
        association_table.c.students_id == 1,
    )
    result = db.execute(query).one_or_none()
    assert response.status_code == 204
    assert result is None

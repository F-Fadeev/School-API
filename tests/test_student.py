from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from source.api.schemas.students_schemas import StudentScheme
from source.db.models import Student


def test_get_students(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.get('/api/students', headers={'Authorization': f'Bearer {get_token}'})
    query = select(Student)
    result = db.execute(query).scalars().all()
    assert response.status_code == 200
    assert len(response.json()) == len(result)


def test_get_specific_student(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.get(
        '/api/students/',
        params={'student_id': 1},
        headers={'Authorization': f'Bearer {get_token}'},
    )
    query = select(Student).filter_by(id=1)
    result = db.execute(query).scalars().first()
    assert response.status_code == 200
    assert response.json()[0] == StudentScheme.from_orm(result).dict()


def test_create_student(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.post(
        '/api/students/create',
        json={
            'group_id': 1,
            'first_name': 'test2',
            'last_name': 'test2',
            'middle_name': 'test2',
        },
        headers={'Authorization': f'Bearer {get_token}'},
    )
    query = select(Student).filter_by(id=2)
    result = db.execute(query).scalars().first()
    assert response.status_code == 201
    assert response.json() == StudentScheme.from_orm(result).dict()


def test_delete_student(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.delete(
        '/api/students/delete/1',
        headers={'Authorization': f'Bearer {get_token}'},
    )
    data = select(Student).filter_by(id=1)
    result = db.execute(data).scalars().first()
    assert response.status_code == 204
    assert result is None


def test_update_student(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.put(
        '/api/students/update/1',
        json={
            'group_id': 1,
            'first_name': 'test2',
            'last_name': 'test2',
            'middle_name': 'test2',
        },
        headers={'Authorization': f'Bearer {get_token}'})
    data = select(Student).filter_by(id=1)
    result = db.execute(data).scalars().first()
    assert response.status_code == 202
    assert response.json() == StudentScheme.from_orm(result).dict()

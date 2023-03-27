from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from source.api.schemas.groups_schemas import GroupScheme
from source.db.models import Group, Student


def test_get_groups(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.get(
        '/api/groups',
        headers={'Authorization': f'Bearer {get_token}'}
    )
    query = select(Group)
    result = db.execute(query).scalars().all()
    assert response.status_code == 200
    assert len(response.json()) == len(result)


def test_get_specific_group(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.get(
        '/api/groups/',
        params={'group_id': 1},
        headers={'Authorization': f'Bearer {get_token}'}
    )
    query = select(Group).filter_by(id=1)
    result = db.execute(query).scalars().first()
    assert response.status_code == 200
    assert response.json()[0] == GroupScheme.from_orm(result).dict()


def test_create_group(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.post(
        '/api/groups/create',
        json={'name': 'test2'},
        headers={'Authorization': f'Bearer {get_token}'}
    )
    query = select(Group).filter_by(id=2)
    result = db.execute(query).scalars().first()
    assert response.status_code == 201
    assert response.json() == GroupScheme.from_orm(result).dict()


def test_delete_group(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.delete(
        '/api/groups/delete/1',
        headers={'Authorization': f'Bearer {get_token}'}
    )
    data = select(Group).filter_by(id=1)
    result = db.execute(data).scalars().first()
    assert response.status_code == 204
    assert result is None


def test_update_group(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.put(
        '/api/groups/update/1',
        json={'name': 'test2'},
        headers={'Authorization': f'Bearer {get_token}'})
    query = select(Group).filter_by(id=1)
    result = db.execute(query).scalars().first()
    assert response.status_code == 202
    assert response.json() == GroupScheme.from_orm(result).dict()


def test_enroll_students(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    client.post(
        '/api/groups/expel/1',
        json={'student_ids': [1]},
        headers={'Authorization': f'Bearer {get_token}'}
    )
    response = client.post(
        '/api/groups/enroll/1',
        json={'student_ids': [1]},
        headers={'Authorization': f'Bearer {get_token}'}
    )
    query = select(Student).filter(and_(Student.group_id == 1, Student.id == 1))
    result = db.execute(query).scalars().first()
    assert response.status_code == 201
    assert response.json() == {'detail': 'Successful'}
    assert result is not None


def test_expel_students(get_client: TestClient, db: Session, get_token: str):
    client = get_client
    response = client.post(
        '/api/groups/expel/1',
        json={'student_ids': [1]},
        headers={'Authorization': f'Bearer {get_token}'}
    )
    query = select(Student).filter(and_(Student.group_id == 1, Student.id == 1))
    result = db.execute(query).scalar_one_or_none()
    assert response.status_code == 204
    assert result is None

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from source.api.schemas.base_schemas import (
    ErrorResponseScheme,
    DefaultResponseScheme,
)
from source.api.schemas.groups_schemas import (
    GroupScheme,
    GroupCreateScheme,
    GroupUpdateScheme,
)
from source.api.schemas.students_schemas import StudentsIdsScheme
from source.api.services.crud.groups.create import CreateGroupService
from source.api.services.crud.groups.delete import DeleteGroupService
from source.api.services.crud.groups.read import (
    GetSpecificGroupService,
    GetFilteredGroupsService,
)
from source.api.services.crud.groups.update import (
    UpdateGroupService,
    EnrollStudentsService,
    ExpelStudentsService,
)
from source.api.services.utils import get_db
from source.db.models import Group

groups_router = APIRouter(prefix='/api/groups', tags=['Groups'])


@groups_router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=list[GroupScheme],
)
def get_all_groups(
    count_students: int = None,
    db: Session = Depends(get_db),
) -> list[GroupScheme]:
    service = GetFilteredGroupsService(db=db, model=Group, count_students=count_students)
    return service()


@groups_router.get(
    '/{group_id}',
    status_code=status.HTTP_200_OK,
    response_model=GroupScheme,
)
def get_specific_group(
    group_id: int,
    db: Session = Depends(get_db),
) -> GroupScheme:
    service = GetSpecificGroupService(db=db, model=Group, group_id=group_id)
    return service()


@groups_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=GroupScheme,
)
def create_group(
    group: GroupCreateScheme,
    db: Session = Depends(get_db),
) -> GroupScheme:
    service = CreateGroupService(db=db, model=Group, scheme=group, return_values=['id', 'name'])
    return service()


@groups_router.delete(
    '/delete/{id_group}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_group(
    id_group: int,
    db: Session = Depends(get_db),
) -> None:
    service = DeleteGroupService(db=db, model=Group, id_group=id_group)
    return service()


@groups_router.put(
    '/update/{id_group}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=GroupScheme,
)
def update_group(
    id_group: int,
    scheme: GroupUpdateScheme,
    db: Session = Depends(get_db),
) -> None | GroupScheme:
    service = UpdateGroupService(db=db, model=Group, scheme=scheme, id_group=id_group, return_values=['id', 'name'])
    return service()


@groups_router.post(
    '/enroll/{id_group}',
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponseScheme}},
    response_model=DefaultResponseScheme,
)
def enrolling_students_to_group(
    id_group: int,
    id_students: StudentsIdsScheme,
    db: Session = Depends(get_db),
) -> dict:
    service = EnrollStudentsService(db=db, model=Group, id_group=id_group, id_students=id_students)
    return service()


@groups_router.post(
    '/expel/{id_group}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponseScheme}},
    response_model=None,
)
def expel_students_from_group(
    id_group: int,
    id_students: StudentsIdsScheme,
    db: Session = Depends(get_db),
) -> None:
    service = ExpelStudentsService(db=db, model=Group, id_group=id_group, id_students=id_students)
    return service()

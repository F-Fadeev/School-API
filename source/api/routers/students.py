from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from source.api.auth.auth_bearer import JWTBearer
from source.api.schemas.students_schemas import (
    StudentScheme,
    StudentCreateScheme,
    StudentUpdateScheme,
    StudentFilters,
)
from source.api.services.crud.students.create import CreateStudentService
from source.api.services.crud.students.delete import DeleteStudentService
from source.api.services.crud.students.read import (
    GetFilteredStudentsService,
    GetSpecificStudentService,
)
from source.api.services.crud.students.update import UpdateStudentService
from source.api.services.utils import get_db
from source.db.models import Student

students_router = APIRouter(
    prefix='/api/students',
    tags=['Students'],
    dependencies=[Depends(JWTBearer())],
)


@students_router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=list[StudentScheme],
)
def get_all_students(
    filter_param: StudentFilters = Depends(StudentFilters),
    db: Session = Depends(get_db),
) -> list[StudentScheme]:
    service = GetFilteredStudentsService(
        db=db,
        model=Student,
        filter_param=filter_param,
    )
    return service()


@students_router.get(
    '/{student_id}',
    status_code=status.HTTP_200_OK,
    response_model=StudentScheme,
)
def get_specific_student(
    student_id: int,
    db: Session = Depends(get_db),
) -> StudentScheme:
    service = GetSpecificStudentService(
        db=db,
        model=Student,
        student_id=student_id,
    )
    return service()


@students_router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=StudentScheme,
)
def create_student(
    student: StudentCreateScheme,
    db: Session = Depends(get_db),
) -> StudentScheme:
    service = CreateStudentService(
        db=db,
        model=Student,
        scheme=student,
        return_values=('id', 'group_id', 'first_name', 'last_name', 'middle_name'),
    )
    return service()


@students_router.delete(
    '/delete/{id_student}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_student(
    id_student: int,
    db: Session = Depends(get_db),
) -> None:
    service = DeleteStudentService(
        db=db,
        model=Student,
        id_student=id_student,
    )
    return service()


@students_router.put(
    '/update/{id_student}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=StudentScheme,
)
def update_student(
    id_student: int,
    scheme: StudentUpdateScheme,
    db: Session = Depends(get_db),
) -> None | StudentScheme:
    service = UpdateStudentService(
        model=Student,
        db=db,
        scheme=scheme,
        id_student=id_student,
        return_values=('id', 'group_id', 'first_name', 'last_name', 'middle_name'),
    )
    return service()

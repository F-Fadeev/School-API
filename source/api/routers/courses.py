from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from source.api.auth.auth_bearer import JWTBearer
from source.api.schemas.base_schemas import (
    DefaultResponseScheme,
    ErrorResponseScheme,
)
from source.api.schemas.courses_schemas import (
    CourseScheme,
    CourseCreateScheme,
    CourseUpdateScheme,
)
from source.api.schemas.students_schemas import StudentsIdsScheme
from source.api.services.crud.courses.create import (
    EnrolCourseService,
    CreateCourseService,
)
from source.api.services.crud.courses.delete import (
    ExpelCourseService,
    DeleteCourseService,
)
from source.api.services.crud.courses.read import (
    GetFilteredCoursesService,
    GetSpecificCourseService,
)
from source.api.services.crud.courses.update import UpdateCourseService
from source.api.services.utils import get_db
from source.db.models import Course

courses_router = APIRouter(prefix='/api/courses', tags=['Courses'], dependencies=[Depends(JWTBearer())])


@courses_router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=list[CourseScheme],
)
def get_all_courses(
    count_students: int = None,
    db: Session = Depends(get_db),
) -> list[CourseScheme]:
    service = GetFilteredCoursesService(db=db, model=Course, count_students=count_students)
    return service()


@courses_router.get(
    '/{course_id}',
    status_code=status.HTTP_200_OK,
    response_model=CourseScheme,
)
def get_specific_course(
    course_id: int,
    db: Session = Depends(get_db),
) -> CourseScheme:
    service = GetSpecificCourseService(db=db, model=Course, course_id=course_id)
    return service()


@courses_router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=CourseScheme,
)
def create_course(
    scheme: CourseCreateScheme,
    db: Session = Depends(get_db),
) -> CourseScheme:
    service = CreateCourseService(db=db, model=Course, scheme=scheme, return_values=['id', 'name', 'description'])
    return service()


@courses_router.delete(
    '/delete/{id_course}',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_course(
    id_course: int,
    db: Session = Depends(get_db),
) -> None:
    service = DeleteCourseService(db=db, model=Course, id_course=id_course)
    return service()


@courses_router.put(
    '/update/{id_course}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CourseScheme,
)
def update_course(
    id_course: int,
    scheme: CourseUpdateScheme,
    db: Session = Depends(get_db),
) -> None | CourseScheme:
    service = UpdateCourseService(
        model=Course,
        db=db,
        scheme=scheme,
        id_course=id_course,
        return_values=['id', 'name', 'description'],
    )

    return service()


@courses_router.post(
    '/enroll/{id_course}',
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponseScheme}},
    response_model=DefaultResponseScheme,
)
def enrolling_students_to_course(
    id_course: int,
    id_students: StudentsIdsScheme,
    db: Session = Depends(get_db),
) -> dict:
    service = EnrolCourseService(
        db=db,
        model=Course,
        id_students=id_students,
        id_course=id_course,
    )
    return service()


@courses_router.delete(
    '/expel/{id_course}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponseScheme}},
    response_model=None,
)
def expel_students_from_course(
        id_course: int,
        id_students: StudentsIdsScheme,
        db: Session = Depends(get_db),
) -> None:
    service = ExpelCourseService(
        db=db,
        model=Course,
        id_students=id_students,
        id_course=id_course,
    )
    return service()

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from starlette import status

from source.api.schemas.students_schemas import StudentsIdsScheme
from source.api.services.crud.base_crud import BaseServices, Model
from source.db.models import association_table, Student


class ExpelUserCoursesService(BaseServices):

    def __init__(self, db: Session, model: Model, id_students: StudentsIdsScheme, id_course: int):

        super().__init__(db, model)
        self.id_students = id_students
        self.id_course = id_course

    def _validate(self) -> None:
        self.data = self._check_course()
        new_students = self._check_new_students()
        students_data = self._check_students(new_students)
        self.data.students.extend(students_data)

    def _execute(self) -> dict:
        self.db.commit()
        return {'detail': 'Successful'}

    def _check_course(self):
        query = select(self.model).filter_by(id_course=self.id_course)
        course_data = self.db.execute(query).scalar_one_or_none()
        if not course_data:
            raise HTTPException(
                detail="Course don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return course_data

    def _check_new_students(self) -> set:
        query = select(association_table).filter_by(course_id=self.id_course)
        enrolled_students = self.db.execute(query).scalars().all()
        new_students = set(self.id_students.student_ids).difference(enrolled_students)
        if not new_students:
            raise HTTPException(
                detail='Students already enrolled',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return new_students

    def _check_students(self, new_students: set):
        query = select(Student).filter(Student.id.in_(new_students))
        students_data = self.db.execute(query).scalars().all()

        if len(students_data) != len(new_students):
            raise HTTPException(
                detail="Some students don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return students_data


class DeleteCourseService(BaseServices):

    def __init__(self, db: Session, model: Model, id_course: int):
        super().__init__(db, model)
        self.id_course = id_course

    def _validate(self) -> None:
        return

    def _execute(self) -> None:
        data = delete(self.model).where(self.model.id == self.id_course)
        self.db.execute(data)
        self.db.commit()
        return

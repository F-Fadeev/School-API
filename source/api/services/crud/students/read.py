from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from source.api.schemas.students_schemas import StudentFilters, StudentScheme
from source.api.services.crud.base_crud import BaseServices, Model
from source.db.models import Course


class GetFilteredStudentsService(BaseServices):
    def __init__(self, db: Session, model: Model, filter_param: StudentFilters):
        super().__init__(db, model)
        self.filter_param = filter_param

    def _validate(self) -> None:
        pass

    def _execute(self) -> Any:
        filters = self.filter_param.dict(exclude_none=True)
        query_filter = []
        for key in filters:
            if key in {'first_name', 'last_name', 'middle_name'}:
                query_filter.append(getattr(self.model, key).ilike(f'%{filters[key]}%'))
            elif key == 'group_id':
                query_filter.append(self.model.group_id == filters[key])
            elif key == 'course_id':
                query_filter.append(self.model.courses.any(Course.id == filters[key]))
        query = select(self.model).filter(and_(True, *query_filter))
        return self.db.execute(query).scalars().all()


class GetSpecificStudentService(BaseServices):
    def __init__(self, db: Session, model: Model, student_id: int):
        super().__init__(db, model)
        self.student_id = student_id

    def _validate(self) -> None:
        self._check_student()

    def _execute(self) -> Any:
        query = select(self.model).filter_by(id=self.student_id)
        result = self.db.execute(query).scalar()
        return result

    def _check_student(self):
        data = select(self.model).filter_by(id=self.student_id)
        student = self.db.execute(data).scalar_one_or_none()
        if not student:
            raise HTTPException(
                detail='Student not found',
                status_code=status.HTTP_404_NOT_FOUND,
            )


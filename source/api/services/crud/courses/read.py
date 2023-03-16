from fastapi import HTTPException, status
from sqlalchemy import select, func, ScalarResult, Sequence
from sqlalchemy.orm import Session

from source.api.services.crud.base_crud import BaseServices, Model
from source.db.models import association_table


class GetFilteredCoursesService(BaseServices):

    def __init__(self, db: Session, model: Model, count_students: int) -> None:
        super().__init__(db, model)
        self.count_students = count_students

    def _validate(self) -> None:
        return

    def _execute(self) -> Sequence:
        query = select(self.model)
        if self.count_students:
            filter_ = (
                select(association_table.c.course_id)
                .having(func.count(association_table.c.students_id) <= self.count_students)
                .group_by(association_table.c.course_id)
            )
            query = query.filter(self.model.id.in_(filter_))
        return self.db.execute(query).scalars().all()


class GetSpecificCourseService(BaseServices):

    def __init__(self, db: Session, model: Model, course_id: int) -> None:
        super().__init__(db, model)
        self.course_id = course_id

    def _validate(self) -> None:
        data = select(self.model).filter_by(id=self.course_id)
        course = self.db.execute(data).scalar_one_or_none()
        if not course:
            raise HTTPException(
                detail='Course not found',
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def _execute(self) -> ScalarResult:
        query = select(self.model).filter_by(id=self.course_id)
        return self.db.execute(query).scalars().first()



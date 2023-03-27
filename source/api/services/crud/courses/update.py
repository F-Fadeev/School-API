from fastapi import HTTPException, status
from sqlalchemy import update, select, Row
from sqlalchemy.orm import Session

from source.api.schemas.courses_schemas import CourseUpdateScheme
from source.api.services.crud.base_crud import BaseServices, Model


class UpdateCourseService(BaseServices):

    def __init__(
        self,
        db: Session,
        model: Model,
        return_values: tuple,
        scheme: CourseUpdateScheme,
        id_course: int,
    ) -> None:
        super().__init__(db, model)

        self.return_values = return_values
        self.scheme = scheme
        self.id_course = id_course

    def _validate(self) -> None:
        data = select(self.model).filter_by(id=self.id_course)
        course = self.db.execute(data).scalar_one_or_none()
        if not course:
            raise HTTPException(
                detail='Course not found',
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def _execute(self) -> Row:
        fields = [getattr(self.model, value) for value in self.return_values]
        scheme = self.scheme.dict(exclude_none=True)
        data = update(self.model).filter(self.model.id == self.id_course).values(**scheme).returning(*fields)
        result = self.db.execute(data).one()
        self.db.commit()
        return result

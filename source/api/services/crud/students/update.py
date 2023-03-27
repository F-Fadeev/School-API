from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import update, select
from sqlalchemy.orm import Session

from source.api.schemas.students_schemas import StudentUpdateScheme
from source.api.services.crud.base_crud import BaseServices, Model
from source.db.models import Group


class UpdateStudentService(BaseServices):
    def __init__(
        self,
        db: Session,
        model: Model,
        scheme: StudentUpdateScheme,
        return_values: tuple,
        id_student: int,
    ) -> None:
        super().__init__(db, model)
        self.scheme = scheme
        self.return_values = return_values
        self.id_student = id_student

    def _validate(self) -> None:
        self._check_student()
        self._check_group()

    def _execute(self) -> Any:
        fields = [getattr(self.model, value) for value in self.return_values]
        scheme = self.scheme.dict(exclude_none=True)
        if scheme:
            data = update(self.model).where(self.model.id == self.id_student).values(**scheme).returning(*fields)
            result = self.db.execute(data).one()
            self.db.commit()
            return result
        return None

    def _check_group(self) -> None:
        if self.scheme.group_id is not None:
            query = select(Group).filter_by(id=self.scheme.group_id)
            group_data = self.db.execute(query).one_or_none()
            if not group_data:
                raise HTTPException(
                    detail="Group don't found",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

    def _check_student(self) -> None:
        data = select(self.model).filter(self.model.id == self.id_student)
        result = self.db.execute(data).scalar_one_or_none()
        if not result:
            raise HTTPException(
                detail='Student not found',
                status_code=status.HTTP_404_NOT_FOUND,
            )

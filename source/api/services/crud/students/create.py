from fastapi import HTTPException, status
from sqlalchemy import insert, Row, select
from sqlalchemy.orm import Session

from source.api.schemas.students_schemas import StudentCreateScheme, StudentScheme
from source.api.services.crud.base_crud import BaseServices, Model
from source.db.models import Group


class CreateStudentService(BaseServices):
    def __init__(
        self,
        db: Session,
        model: Model,
        return_values: list[str],
        scheme: StudentCreateScheme,
    ) -> None:
        super().__init__(db, model)
        self.return_values = return_values
        self.scheme = scheme

    def _validate(self) -> None:
        self._check_group()

    def _execute(self) -> Row:
        fields = [getattr(self.model, value) for value in self.return_values]
        data = insert(self.model).values(**self.scheme.dict()).returning(*fields)
        result = self.db.execute(data).one()
        self.db.commit()
        return result

    def _check_group(self):
        if self.scheme.group_id is not None:
            query = select(Group).filter_by(id=self.scheme.group_id)
            group_data = self.db.execute(query).scalar_one_or_none()
            if not group_data:
                raise HTTPException(
                    detail="Group don't found",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

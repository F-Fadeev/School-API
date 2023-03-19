from sqlalchemy import insert, Row
from sqlalchemy.orm import Session

from source.api.schemas.students_schemas import StudentCreateScheme
from source.api.services.crud.base_crud import BaseServices, Model


class CreateStudentService(BaseServices):
    def __init__(
        self,
        db: 'Session',
        model: Model,
        return_values: list[str],
        scheme: 'StudentCreateScheme',
    ) -> None:
        super().__init__(db, model)
        self.return_values = return_values
        self.scheme = scheme

    def _validate(self) -> None:
        pass

    def _execute(self) -> Row:
        fields = [getattr(self.model, value) for value in self.return_values]
        data = insert(self.model).values(**self.scheme.dict()).returning(*fields)
        result = self.db.execute(data).one()
        self.db.commit()
        return result


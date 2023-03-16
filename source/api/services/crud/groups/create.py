from sqlalchemy import insert, Row
from sqlalchemy.orm import Session

from source.api.services.crud.base_crud import BaseServices, Model
from source.api.schemas.groups_schemas import GroupCreateScheme




class CreateGroupService(BaseServices):
    def __init__(
        self,
        db: Session,
        model: Model,
        return_values: list[str],
        scheme: GroupCreateScheme,
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

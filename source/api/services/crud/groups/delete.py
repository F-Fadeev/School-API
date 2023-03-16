from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from source.api.services.crud.base_crud import BaseServices, Model



class DeleteGroupService(BaseServices):
    def __init__(self, db: Session, model: Model, id_group: int):
        super().__init__(db, model)
        self.id_group = id_group

    def _validate(self) -> None:
        data = select(self.model).filter(self.model.id == self.id_group)
        group = self.db.execute(data).scalar_one_or_none()
        if not group:
            raise HTTPException(
                detail='Group not found',
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def _execute(self) -> None:
        data = delete(self.model).filter(self.model.id == self.id_group)
        self.db.execute(data)
        self.db.commit()



from fastapi import HTTPException, status
from sqlalchemy import select, func, ScalarResult, Sequence
from sqlalchemy.orm import Session

from source.api.services.crud.base_crud import BaseServices, Model
from source.db.models import Student


class GetFilteredGroupsService(BaseServices):
    def __init__(self, db: Session, model: Model, count_students: int) -> None:
        super().__init__(db, model)
        self.count_students = count_students

    def _validate(self) -> None:
        pass

    def _execute(self) -> Sequence:
        if self.count_students:
            query = select(self.model) \
                .join(self.model.students) \
                .group_by(self.model.id) \
                .having(func.count(Student.id) <= self.count_students)
            return self.db.execute(query).scalars().all()
        query = select(self.model)
        return self.db.execute(query).scalars().all()


class GetSpecificGroupService(BaseServices):
    def __init__(self, db: Session, model: Model, group_id: int) -> None:
        super().__init__(db, model)
        self.group_id = group_id
        self.model = model
        self.db = db

    def _validate(self) -> None:
        data = select(self.model).filter(self.model.id == self.group_id)
        group = self.db.execute(data).scalar_one_or_none()
        if not group:
            raise HTTPException(
                detail='Group not found',
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def _execute(self) -> ScalarResult:
        query = select(self.model).filter(self.model.id == self.group_id)
        return self.db.execute(query).scalars().first()

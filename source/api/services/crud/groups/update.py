from fastapi import HTTPException, status
from sqlalchemy import update, select, Row, RowMapping, Sequence
from sqlalchemy.orm import Session

from source.api.schemas.groups_schemas import GroupUpdateScheme
from source.api.schemas.students_schemas import StudentsIdsScheme
from source.api.services.crud.base_crud import BaseServices, Model
from source.db.models import Student


class UpdateGroupService(BaseServices):
    def __init__(
        self,
        db: Session,
        model: Model,
        return_values: tuple,
        scheme: GroupUpdateScheme,
        id_group: int,
    ) -> None:
        super().__init__(db, model)
        self.return_values = return_values
        self.scheme = scheme
        self.id_group = id_group

    def _validate(self) -> None:
        data = select(self.model).filter(self.model.id == self.id_group)
        group = self.db.execute(data).scalar_one_or_none()
        if not group:
            raise HTTPException(
                detail='Group not found',
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def _execute(self) -> Row | None:
        fields = [getattr(self.model, value) for value in self.return_values]
        scheme = self.scheme.dict(exclude_none=True)
        if scheme:
            data = (update(self.model)
                    .where(self.model.id == self.id_group)
                    .values(**scheme).returning(*fields))
            result = self.db.execute(data).one()
            self.db.commit()
            return result
        return None


class EnrollStudentsService(BaseServices):
    def __init__(
        self,
        db: Session,
        model: Model,
        id_group: int,
        id_students: StudentsIdsScheme,
    ) -> None:
        super().__init__(db, model)
        self.id_group = id_group
        self.id_students = id_students

    def _validate(self) -> None:
        self.data = self._check_group()
        new_students = self._check_new_students()
        students_data = self._check_students(new_students)
        self.data.students.extend(students_data)

    def _execute(self) -> dict:
        self.db.commit()
        return {'detail': 'Successful'}

    def _check_group(self) -> Row:
        query = select(self.model).filter_by(id=self.id_group)
        group_data = self.db.execute(query).scalar_one_or_none()
        if not group_data:
            raise HTTPException(
                detail="Group don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return group_data

    def _check_new_students(self) -> set[int]:
        query = select(Student.id).filter_by(group_id=self.id_group)
        enrolled_students = self.db.execute(query).scalars().all()
        new_students = set(self.id_students.student_ids).difference(enrolled_students)
        if not new_students:
            raise HTTPException(
                detail='Students already in this group',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return new_students

    def _check_students(self, new_students: set) -> Sequence:
        query = select(Student).filter(Student.id.in_(new_students))
        students_data = self.db.execute(query).scalars().all()
        if len(students_data) != len(new_students):
            raise HTTPException(
                detail="Some students don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return students_data


class ExpelStudentsService(BaseServices):
    def __init__(
        self,
        db: Session,
        model: Model,
        id_students: StudentsIdsScheme,
        id_group: int,
    ):
        super().__init__(db, model)
        self.id_students = id_students
        self.id_group = id_group

    def _validate(self) -> None:
        group_data = self.data = self._check_group()
        self._check_students()
        updated_enrolled_students = self._check_enrolled_students()
        students_data = self.db.query(Student).filter(Student.id.in_(updated_enrolled_students)).all()
        group_data.students = students_data

    def _execute(self) -> None:
        self.db.commit()

    def _check_group(self) -> Row:
        query = select(self.model).filter_by(id=self.id_group)
        group_data = self.db.execute(query).scalar_one_or_none()
        if not group_data:
            raise HTTPException(
                detail="Group don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return group_data

    def _check_students(self) -> None:
        query = select(Student.id).filter(Student.id.in_(self.id_students.student_ids))
        check_students = self.db.execute(query).scalars().all()
        if len(check_students) != len(self.id_students.student_ids):
            raise HTTPException(
                detail="Some students don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def _check_enrolled_students(self) -> set[Row, RowMapping]:
        query = select(Student.id).filter_by(group_id=self.id_group)
        enrolled_students = self.db.execute(query).scalars().all()
        updated_enrolled_students = set(enrolled_students).difference(set(self.id_students.student_ids))
        if len(updated_enrolled_students) == len(enrolled_students):
            raise HTTPException(
                detail='These students are not in this group anyway',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return updated_enrolled_students


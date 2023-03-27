from abc import ABC, abstractmethod
from typing import TypeVar, Any

from sqlalchemy.orm import Session

from source.db.models import (
    Student,
    Group,
    Course,
    association_table,
)

Model = TypeVar('Model', type[Student], type[Group], type[Course], type[association_table])


class BaseServices(ABC):

    def __init__(self, db: 'Session', model: Model) -> None:
        self.db = db
        self.model = model
        self.data = None

    def __call__(self) -> Any:
        self._validate()
        return self._execute()

    @abstractmethod
    def _validate(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _execute(self) -> Any:
        raise NotImplementedError

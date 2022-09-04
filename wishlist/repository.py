from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from sqlalchemy.orm import Session

from wishlist import exc, models

M = TypeVar("M")


class Repository(ABC, Generic[M]):
    @abstractmethod
    def add(self, model: M) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get(self, id_: int) -> M:
        raise NotImplementedError()

    @abstractmethod
    def optional(self, id_: int) -> M | None:
        raise NotImplementedError()

    @abstractmethod
    def list_(self) -> List[M]:
        raise NotImplementedError()


class SQLAlchemyRepository(Repository, Generic[M]):
    def __init__(self, session: Session) -> None:
        self.session = session

    @abstractmethod
    def _model(self) -> M:
        raise NotImplementedError()

    def add(self, model: M) -> None:
        return self.session.add(model)

    def optional(self, id_: int) -> M | None:
        return self.session.query(self._model()).get(id_)

    def get(self, id_: int) -> M:

        model = self.optional(id_)
        if model is None:
            raise exc.NotFound()

        return model

    def list_(self) -> List[M]:
        return self.session.query(self._model()).all()


class SQLAlchemyWishlistRepository(SQLAlchemyRepository[models.Wishlist]):
    def _model(self) -> models.Wishlist:
        return models.Wishlist


class SQLAlchemyUserRepository(SQLAlchemyRepository[models.User]):
    def _model(self) -> models.User:
        return models.User

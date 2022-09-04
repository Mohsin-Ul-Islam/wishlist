from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy.orm import Session, sessionmaker

from wishlist.models import Wishlist
from wishlist.orm import DEFAULT_SESSION_FACTORY
from wishlist.repository import Repository, SQLAlchemyWishlistRepository


class UnitOfWork(ABC):

    wishlists: Repository[Wishlist]

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError()

    def __enter__(self) -> UnitOfWork:
        raise NotImplementedError()

    def __exit__(self, exc_t, exc_val, exc_tb) -> None:

        if exc_t or exc_val or exc_tb:
            return self.rollback()

        return self.commit()


class SQLAlchemyUnitOfWork(UnitOfWork):

    session: Session

    def __init__(self, session_factory: sessionmaker = DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory = session_factory

    def __enter__(self) -> SQLAlchemyUnitOfWork:

        self.session = DEFAULT_SESSION_FACTORY()
        self.wishlists = SQLAlchemyWishlistRepository(session=self.session)

        return self

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

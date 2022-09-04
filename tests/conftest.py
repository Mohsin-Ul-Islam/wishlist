from os import environ

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm import Session
from testing.postgresql import Postgresql

database = Postgresql()


def pytest_sessionstart(session):
    database.start()
    environ["DATABASE_URL"] = database.url()


def pytest_sessionfinish(session):
    database.stop()


@fixture(scope="session")
def client() -> TestClient:
    from wishlist.app import app  # noqa

    return TestClient(app)


@fixture(scope="session")
def session() -> Session:
    from wishlist.orm import DEFAULT_SESSION_FACTORY

    return DEFAULT_SESSION_FACTORY()


@fixture(scope="function", autouse=True)
def clear_database() -> None:

    from wishlist.orm import engine, mapper_registry

    for table in reversed(mapper_registry.metadata.sorted_tables):
        engine.execute(f"truncate {table.name} restart identity cascade;")

import jwt
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from wishlist import __version__, models


def _get_token(id_: int) -> str:
    return jwt.encode({"user_id": id_}, "s3cr3t", "HS256")


def test_version():
    assert __version__ == "0.1.1"


def test_get_wishlist_by_id_no_auth(client: TestClient) -> None:
    assert client.get("/api/v1/wishlists/1").status_code == 403


def test_get_user_wishlists_no_auth(client: TestClient) -> None:
    assert client.get("/api/v1/users/1/wishlists").status_code == 403


def test_non_existent_get_wishlist_by_id(client: TestClient, session: Session) -> None:

    with session:
        session.add(models.User(id_=1))
        session.commit()

    assert (
        client.get(
            "/api/v1/wishlists/1", headers={"Authorization": f"Bearer {_get_token(1)}"}
        ).status_code
        == 404
    )


def test_non_existent_user_wishlist(client: TestClient, session: Session) -> None:

    with session:
        session.add(models.User(id_=1))
        session.commit()

    response = client.get(
        "/api/v1/users/1/wishlists",
        headers={"Authorization": f"Bearer {_get_token(1)}"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_user_wishlists(client: TestClient, session: Session) -> None:

    with session:
        session.add(models.User(id_=1))
        session.add(
            models.Wishlist(
                id_=1,
                user_id=1,
                lines=[models.WishlistLine(product_id=1, wishlist_id=1)],
            )
        )
        session.add(
            models.Wishlist(
                id_=2,
                user_id=1,
                lines=[models.WishlistLine(product_id=1, wishlist_id=2)],
            )
        )
        session.commit()

    response = client.get(
        "/api/v1/users/1/wishlists",
        headers={"Authorization": f"Bearer {_get_token(1)}"},
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id_": 1,
            "user_id": 1,
            "lines": [
                {
                    "product_id": 1,
                    "wishlist_id": 1,
                }
            ],
        },
        {
            "id_": 2,
            "user_id": 1,
            "lines": [
                {
                    "product_id": 1,
                    "wishlist_id": 2,
                }
            ],
        },
    ]


def test_get_wishlist_by_id(client: TestClient, session: Session) -> None:

    with session:
        session.add(models.User(id_=1))
        session.add(
            models.Wishlist(
                id_=1,
                user_id=1,
                lines=[models.WishlistLine(product_id=1, wishlist_id=1)],
            )
        )
        session.commit()

    response = client.get(
        "/api/v1/wishlists/1", headers={"Authorization": f"Bearer {_get_token(1)}"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "id_": 1,
        "user_id": 1,
        "lines": [
            {
                "product_id": 1,
                "wishlist_id": 1,
            }
        ],
    }


def test_add_line_to_wishlist(client: TestClient, session: Session) -> None:

    with session:
        session.add(models.User(id_=1))
        session.add(
            models.Wishlist(
                id_=1,
                user_id=1,
                lines=[models.WishlistLine(product_id=1, wishlist_id=1)],
            )
        )
        session.commit()

    response = client.post(
        "/api/v1/wishlists/1",
        json={"product_id": 2, "wishlist_id": 1},
        headers={"Authorization": f"Bearer {_get_token(1)}"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id_": 1,
        "user_id": 1,
        "lines": [
            {
                "product_id": 1,
                "wishlist_id": 1,
            },
            {
                "product_id": 2,
                "wishlist_id": 1,
            },
        ],
    }


def test_remove_line_from_wishlist(client: TestClient, session: Session) -> None:

    with session:
        session.add(models.User(id_=1))
        session.add(
            models.Wishlist(
                id_=1,
                user_id=1,
                lines=[models.WishlistLine(product_id=1, wishlist_id=1)],
            )
        )
        session.commit()

    response = client.delete(
        "/api/v1/wishlists/1/lines/1",
        headers={"Authorization": f"Bearer {_get_token(1)}"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "id_": 1,
        "user_id": 1,
        "lines": [],
    }

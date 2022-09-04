from os import environ

from sqlalchemy import BigInteger, Column, ForeignKey, Table, create_engine
from sqlalchemy.orm import registry, relationship, sessionmaker

from wishlist import models

engine = create_engine(environ["DATABASE_URL"])

DEFAULT_SESSION_FACTORY = sessionmaker(bind=engine)

mapper_registry = registry()

users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", BigInteger, key="id_", primary_key=True, autoincrement=True),
)

wishlist_table = Table(
    "wishlists",
    mapper_registry.metadata,
    Column("id", BigInteger, key="id_", primary_key=True, autoincrement=True),
    Column("user_id", BigInteger, ForeignKey("users.id_")),
)

wishlist_line_table = Table(
    "wishlist_lines",
    mapper_registry.metadata,
    Column("product_id", BigInteger, primary_key=True, autoincrement=False),
    Column(
        "wishlist_id",
        BigInteger,
        ForeignKey("wishlists.id_"),
        primary_key=True,
        autoincrement=False,
    ),
)

mapper_registry.map_imperatively(models.User, users_table)
mapper_registry.map_imperatively(
    models.Wishlist,
    wishlist_table,
    properties={
        "lines": relationship(models.WishlistLine, lazy="joined", collection_class=set)
    },
)
mapper_registry.map_imperatively(models.WishlistLine, wishlist_line_table)
mapper_registry.metadata.create_all(engine)

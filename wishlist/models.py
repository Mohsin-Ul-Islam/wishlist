from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    id_: int


@dataclass
class AuthUser:
    id_: int
    access_token: str
    refresh_token: str


@dataclass
class AuthRequest:
    username: str
    password: str


@dataclass
class WishlistLine:
    product_id: int
    wishlist_id: int


@dataclass
class Wishlist:
    id_: int
    user_id: int
    lines: List[WishlistLine] = field(default_factory=list)

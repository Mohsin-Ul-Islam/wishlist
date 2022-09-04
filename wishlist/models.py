from dataclasses import dataclass, field
from typing import Set


@dataclass
class User:
    id_: int


@dataclass
class WishlistLine:
    product_id: int
    wishlist_id: int

    def __hash__(self) -> int:
        return hash((self.product_id, self.wishlist_id))


@dataclass
class Wishlist:
    id_: int
    user_id: int
    lines: Set[WishlistLine] = field(default_factory=set)

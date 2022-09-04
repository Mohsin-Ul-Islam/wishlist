from typing import List

from wishlist.exc import NotFound
from wishlist.models import Wishlist
from wishlist.orm import DEFAULT_SESSION_FACTORY


def get_user_wishlists(user_id: int) -> List[Wishlist]:

    with DEFAULT_SESSION_FACTORY() as session:
        return session.query(Wishlist).all()


def get_wishlist_by_id(wishlist_id: int) -> Wishlist:

    with DEFAULT_SESSION_FACTORY() as session:

        wishlist = session.query(Wishlist).get(wishlist_id)
        if wishlist is None:
            raise NotFound()

        return wishlist

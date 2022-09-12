from wishlist.models import Wishlist, WishlistLine
from wishlist.uow import UnitOfWork


def add_item_to_wishlist(
    uow: UnitOfWork, wishlist_id: int, line: WishlistLine
) -> Wishlist:

    line.wishlist_id = wishlist_id
    with uow:
        wishlist = uow.wishlists.get(wishlist_id)
        wishlist.lines.append(line)
        return wishlist


def remove_item_from_wishlist(
    uow: UnitOfWork, wishlist_id: int, line_id: int
) -> Wishlist:

    with uow:
        wishlist = uow.wishlists.get(wishlist_id)
        wishlist.lines.remove(WishlistLine(line_id, wishlist_id))
        return wishlist

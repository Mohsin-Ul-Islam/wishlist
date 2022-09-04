from typing import List

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from wishlist import commands, exc, queries, uow
from wishlist.models import Wishlist, WishlistLine

app = FastAPI()
uow = uow.SQLAlchemyUnitOfWork()

@app.exception_handler(exc.NotFound)
def handle_not_found(_, exception: exc.NotFound) -> JSONResponse:
    return JSONResponse(content='not found!', status_code=404)

@app.get("/api/v1/users/{user_id}/wishlists")
async def get_user_wishlists(user_id: int) -> List[Wishlist]:
    return queries.get_user_wishlists(user_id)


@app.get("/api/v1/wishlists/{wishlist_id}")
async def get_wishlist_by_id(wishlist_id: int) -> Wishlist:
    return queries.get_wishlist_by_id(wishlist_id)


@app.post("/api/v1/wishlists/{wishlist_id}")
async def add_item_to_wishlist(wishlist_id: int, line: WishlistLine) -> Wishlist:
    return commands.add_item_to_wishlist(uow, wishlist_id, line)


@app.delete("/api/v1/wishlists/{wishlist_id}/lines/{line_id}")
async def remove_item_from_wishlist(wishlist_id: int, line_id: int) -> Wishlist:
    return commands.remove_item_from_wishlist(uow, wishlist_id, line_id)

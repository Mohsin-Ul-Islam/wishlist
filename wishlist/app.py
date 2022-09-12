from typing import List

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from wishlist import commands, exc, queries, uow
from wishlist.auth import JWTBearer, get_current_user
from wishlist.models import AuthRequest, AuthUser, Wishlist, WishlistLine

app = FastAPI()
uow = uow.SQLAlchemyUnitOfWork()


@app.exception_handler(exc.NotFound)
def handle_not_found(_, exception: exc.NotFound) -> JSONResponse:
    return JSONResponse(content=exception.message, status_code=404)


@app.get(
    "/api/v1/users/{user_id}/wishlists",
    response_model=List[Wishlist],
    dependencies=[Depends(JWTBearer())],
)
async def get_user_wishlists(
    user_id: int, user: AuthUser = Depends(get_current_user)
) -> List[Wishlist]:
    return queries.get_user_wishlists(user_id)


@app.get(
    "/api/v1/wishlists/{wishlist_id}",
    response_model=Wishlist,
    dependencies=[Depends(JWTBearer())],
)
async def get_wishlist_by_id(
    wishlist_id: int, user: AuthUser = Depends(get_current_user)
) -> Wishlist:
    return queries.get_wishlist_by_id(wishlist_id)


@app.post(
    "/api/v1/wishlists/{wishlist_id}",
    response_model=Wishlist,
    status_code=201,
    dependencies=[Depends(JWTBearer())],
)
async def add_item_to_wishlist(
    wishlist_id: int, line: WishlistLine, user: AuthUser = Depends(get_current_user)
) -> Wishlist:
    return commands.add_item_to_wishlist(uow, wishlist_id, line)


@app.delete(
    "/api/v1/wishlists/{wishlist_id}/lines/{line_id}",
    status_code=404,
    response_model=Wishlist,
    dependencies=[Depends(JWTBearer())],
)
async def remove_item_from_wishlist(
    wishlist_id: int, line_id: int, user: AuthUser = Depends(get_current_user)
) -> Wishlist:
    return commands.remove_item_from_wishlist(uow, wishlist_id, line_id)


@app.post("/api/v1/auth/login", response_model=AuthUser, status_code=201)
async def login(user: AuthRequest) -> AuthUser:
    return


@app.delete("/api/v1/auth/logout", status_code=404, dependencies=[Depends(JWTBearer())])
async def logout(_: AuthUser = Depends(get_current_user)) -> None:
    return

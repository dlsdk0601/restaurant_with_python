from ex.api import BaseModel, Res, err, ok
from was.blueprints import app, bg
from was.model.asset import Asset
from was.model.user import User


class UserShowReq(BaseModel):
    pass


class UserShowRes(BaseModel):
    pk: int
    email: str
    name: str
    image: Asset.Bsset


@app.api()
def user_show(req: UserShowReq) -> Res[UserShowRes]:
    user: User | None = bg.user

    if user is None:
        return err('유저 정보가 조회되지 않습니다.')

    return ok(UserShowRes(pk=user.pk, email=user.email, name=user.name, image=user.image.to_bsset()))


class BasketListReq(BaseModel):
    pass


class BasketListResItem(BaseModel):
    pk: int
    restaurant_pk: int
    name: str
    priceRange: str
    rating: float
    ratingsCount: int
    deliveryTime: int
    deliverFee: int
    image: Asset.Bsset
    tags: list[str]
    price: int
    detail: str


class BasketListRes(BaseModel):
    products: list[BasketListResItem]

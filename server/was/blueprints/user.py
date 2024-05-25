from ex.api import BaseModel, Res, err, ok
from was.blueprints import app, bg
from was.model import db
from was.model.asset import Asset
from was.model.cart import Cart
from was.model.user import User


class UserShowReq(BaseModel):
    pass


class UserShowRes(BaseModel):
    pk: int
    email: str
    name: str
    image: Asset.Bsset
    cart_count: int


@app.api()
def user_show(req: UserShowReq) -> Res[UserShowRes]:
    user: User | None = bg.user

    if user is None:
        return err('유저 정보가 조회되지 않습니다.')

    if user.cart is None:
        cart = Cart(user=user)
        db.session.add(cart)
        db.session.commit()

    return ok(UserShowRes(
        pk=user.pk, email=user.email, name=user.name,
        image=user.image.to_bsset(), cart_count=user.cart.total_count
    ))


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

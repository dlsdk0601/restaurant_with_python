from sqlalchemy import func

from ex.api import BaseModel, Res, ok, err
from was.blueprints import app, bg
from was.model import db
from was.model.asset import Asset
from was.model.cart import CartItem


class GetCartCountReq(BaseModel):
    pass


class GetCartCountRes(BaseModel):
    cart_count: int


@app.api()
def get_cart_count(req: GetCartCountReq) -> Res[GetCartCountRes]:
    if bg.user is None:
        return err('로그인후 이용해주시기 바랍니다.')

    return ok(GetCartCountRes(cart_count=bg.user.cart.total_count))


class CartAddReq(BaseModel):
    product_pk: int


class CartAddRes(BaseModel):
    cart_count: int


@app.api()
def cart_add(req: CartAddReq) -> Res[CartAddRes]:
    if bg.user is None:
        return err('로그인후 이용해주시기 바랍니다.')

    cart = bg.user.cart
    cart_item = db.session.execute(
        db.select(CartItem).filter_by(product_pk=req.product_pk, cart_pk=cart.pk, delete_at=None)
    ) \
        .scalar_one_or_none()

    if cart_item is not None:
        # 이미 장바구니에 존재
        cart_item.count += 1
    else:
        # 첫 장바구니
        cart.cart_items.append(CartItem(
            product_pk=req.product_pk, count=1,
        ))

    db.session.commit()

    return ok(CartAddRes(cart_count=cart.total_count))


class CartRemoveReq(BaseModel):
    product_pk: int


class CartRemoveRes(BaseModel):
    cart_count: int


@app.api()
def cart_remove(req: CartRemoveReq) -> Res[CartRemoveRes]:
    if bg.user is None:
        return err('로그인후 이용해주시기 바랍니다.')

    cart = bg.user.cart
    cart_item: CartItem | None = db.session.execute(
        db.select(CartItem).filter_by(product_pk=req.product_pk, cart_pk=cart.pk, delete_at=None)
    ) \
        .scalar_one_or_none()

    if cart_item is None:
        # 제거 할때는 장바구니에 무조건 존재해야한다.
        return err('장바구니에서 조회되지 않습니다.')

    if cart_item.count == 1:
        cart_item.delete_at = func.now()
    else:
        cart_item.count -= 1

    db.session.commit()
    return ok(CartRemoveRes(cart_count=cart.total_count))


class CartListReq(BaseModel):
    pass


class CartListResItem(BaseModel):
    pk: int
    image: Asset.Bsset
    name: str
    detail: str
    price: int
    count: int
    product_pk: int

    @classmethod
    def from_model(cls, cart_item: CartItem) -> 'CartListResItem':
        return CartListResItem(
            pk=cart_item.pk, image=cart_item.product.main_image.to_bsset(), name=cart_item.product.name,
            detail=cart_item.product.detail, price=cart_item.product.price, count=cart_item.count,
            product_pk=cart_item.product_pk
        )


class CartListRes(BaseModel):
    total_price: int
    total_delivery_fee: int
    carts: list[CartListResItem]


@app.api()
def cart_list(req: CartListReq) -> Res[CartListRes]:
    if bg.user is None:
        return err('로그인 후 이용가능합니다.')

    cart_items = db.session.execute(
        db.select(CartItem).filter_by(cart_pk=bg.user.cart.pk, delete_at=None)
    ) \
        .all()

    return ok(
        CartListRes(
            total_price=bg.user.cart.total_price,
            total_delivery_fee=bg.user.cart.total_delivery_fee,
            carts=list(map(lambda x: CartListResItem.from_model(x), bg.user.cart.cart_items))
        )
    )

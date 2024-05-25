from ex.api import BaseModel, Res, ok, err
from was.blueprints import app, bg
from was.model import db
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
        db.select(CartItem).filter_by(product_pk=req.product_pk, cart_pk=cart.pk)
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

from random import randint

from sqlalchemy import func

from ex.api import BaseModel, Res, err, ok
from was.blueprints import app, bg
from was.model import db
from was.model.order import OrderState, OrderItem, Order


class AddOrderProductListItem(BaseModel):
    pk: int
    count: int
    price: int


class AddOrderReq(BaseModel):
    total_price: int
    products: list[AddOrderProductListItem]


class AddOrderRes(BaseModel):
    state: OrderState


@app.api()
def add_order(req: AddOrderReq) -> Res[AddOrderRes]:
    if bg.user is None:
        return err('로그인 후 사용가능합니다.')

    order_items = []
    for item in req.products:
        order_item = OrderItem(
            product_pk=item.pk,
            count=item.count, price=item.price
        )
        order_items.append(order_item)

    order = Order(
        state=OrderState.INIT, order_items=order_items,
        total_price=req.total_price, user_pk=bg.user.pk,
    )
    db.session.add(order)

    # pg 사와 연동 해야하는데 안할거임. flutter 연습이기 때문에
    random_int = randint(1, 10)
    if random_int > 5:
        order.state = OrderState.SUCCESS
        for cart_item in bg.user.cart.cart_items:
            cart_item.delete_at = func.now()
    else:
        order.state = OrderState.FAIL

    db.session.commit()

    return ok(AddOrderRes(
        state=order.state
    ))

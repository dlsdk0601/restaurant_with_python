from datetime import datetime
from random import randint

from sqlalchemy import func

from ex.api import BaseModel, Res, err, ok
from ex.sqlalchemy_ex import Pagination, api_paginate
from was.blueprints import app, bg
from was.model import db
from was.model.asset import Asset
from was.model.order import OrderState, OrderItem, Order


class OrderListReq(BaseModel):
    page: int


class OrderListResItem(BaseModel):
    order_date: datetime
    image: Asset.Bsset
    name: str
    product_names: list[str]
    price: int

    @classmethod
    def from_model(cls, order: Order) -> 'OrderListResItem':
        return OrderListResItem(
            order_date=order.create_at, image=order.order_items[0].product.main_image.to_bsset(),
            name=order.restaurant_name, product_names=list(map(lambda x: x.product.name, order.order_items)),
            price=order.total_price
        )


class OrderListRes(BaseModel):
    orders: Pagination[OrderListResItem]


@app.api()
def order_list(req: OrderListReq) -> Res[OrderListRes]:
    q = (
        db
        .select(Order)
        .filter_by(state=OrderState.SUCCESS)
        .order_by(Order.create_at.desc())
    )

    pagination = api_paginate(q, page=req.page, map_=OrderListResItem.from_model)

    return ok(OrderListRes(orders=pagination))


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
    # 일정 확률로 성공 실패를 다 뱉어낸다.
    random_int = randint(1, 10)
    if random_int > 3:
        order.state = OrderState.SUCCESS
        for cart_item in bg.user.cart.cart_items:
            cart_item.delete_at = func.now()
    else:
        order.state = OrderState.FAIL

    db.session.commit()

    return ok(AddOrderRes(
        state=order.state
    ))

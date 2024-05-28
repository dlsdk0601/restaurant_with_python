from datetime import datetime
from enum import auto

from sqlalchemy import DateTime, func, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ex.py.enum_ex import StringEnum
from was.model import Model
from was.model.product import Product
from was.model.user import User


class OrderState(StringEnum):
    INIT = auto()
    SUCCESS = auto()
    FAIL = auto()


class Order(Model):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='PK')
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    state: Mapped[OrderState] = mapped_column(Enum(OrderState), nullable=False, comment='상태')

    user_pk: Mapped[int] = mapped_column(ForeignKey(User.pk), nullable=False, comment='USER - FK')
    user: Mapped[User] = relationship()

    total_price: Mapped[int] = mapped_column(Integer, nullable=False, comment='주문 가격')

    order_items: Mapped[list['OrderItem']] = relationship('OrderItem', back_populates='order')

    __table_args__ = (
        {'comment': '주문'},
    )


class OrderItem(Model):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='PK')

    order_pk: Mapped[int] = mapped_column(ForeignKey(Order.pk), nullable=False, comment='ORDER - FK')
    order: Mapped[Order] = relationship()

    # snap 이기에 product 에서 가격 가져오지 말고 여기 저장한다. 
    price: Mapped[int] = mapped_column(Integer, nullable=False, comment='제품 가격')
    product_pk: Mapped[int] = mapped_column(ForeignKey(Product.pk), nullable=False, comment='PRODUCT - FK')
    product: Mapped[Product] = relationship()
    count: Mapped[int] = mapped_column(Integer, nullable=False, comment='갯수')

    __table_args__ = (
        {'comment': '주문 상품'},
    )

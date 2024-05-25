from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from was.model import Model
from was.model.product import Product
from was.model.user import User


class Cart(Model):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='PK')

    user_pk: Mapped[int] = mapped_column(ForeignKey(User.pk), nullable=False, comment='USER - FK')
    user: Mapped[User] = relationship()

    cart_items: Mapped[list['CartItem']] = relationship('CartItem', back_populates='cart')

    @hybrid_property
    def total_count(self) -> int:
        count = 0
        for item in self.cart_items:
            count += item.count

        return count

    @hybrid_property
    def total_price(self) -> int:
        price = 0
        for item in self.cart_items:
            price += item.count * item.product.price

        return price

    __table_args__ = (
        {'comment': '장바구니'},
    )


class CartItem(Model):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='PK')

    cart_pk: Mapped[int] = mapped_column(ForeignKey(Cart.pk), nullable=False, comment='CART - FK')
    cart: Mapped[Cart] = relationship()

    product_pk: Mapped[int] = mapped_column(ForeignKey(Product.pk), nullable=False, comment='PRODUCT - FK')
    product: Mapped[Product] = relationship()

    count: Mapped[int] = mapped_column(Integer, nullable=False, comment='갯수')
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now(), default=None)
    delete_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    @hybrid_property
    def is_active(self) -> bool:
        return self.delete_at is None

    __table_args__ = (
        {'comment': '장바구니 아이템'},
    )

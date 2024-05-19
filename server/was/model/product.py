from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from was.model import Model
from was.model.asset import Asset
from was.model.restaurant import Restaurant


class Product(Model):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='PK')
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment='제품 이름')
    main_image_pk: Mapped[int] = mapped_column(ForeignKey(Asset.pk), nullable=False, comment='ASSET - FK')
    main_image: Mapped[Asset] = relationship()

    # 어드민을 제작하면 detail 보다는 description 이 맞고, varchar 보다는 Text 타입이 맞다.
    detail: Mapped[str] = mapped_column(String(512), nullable=False, comment='제품 설명')
    price: Mapped[int] = mapped_column(Integer, nullable=False, comment='가격')

    restaurant_pk: Mapped[int] = mapped_column(ForeignKey(Restaurant.pk), nullable=False, comment='레스토랑 - FK')
    restaurant: Mapped[Restaurant] = relationship()
 
    __table_args__ = (
        {'comment': '제품'},
    )

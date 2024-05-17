from enum import auto

from sqlalchemy import String, ForeignKey, Float, Integer
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ex.py.enum_ex import StringEnum
from was.model import Model
from was.model.asset import Asset
from was.model.tag import Tag, RestaurantTag


class RestaurantPriceRange(StringEnum):
    cheap = auto()
    medium = auto()
    expensive = auto()


class Restaurant(Model):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='PK')
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment='레스토랑 이름')
    main_image_pk: Mapped[int] = mapped_column(ForeignKey(Asset.pk), nullable=False, comment='ASSET - FK')
    main_image: Mapped[Asset] = relationship()
    price_range: Mapped[RestaurantPriceRange] = mapped_column(postgresql.ENUM(RestaurantPriceRange), nullable=False,
                                                              comment='가격 수준')

    # 원래 평점은 이런식으로 계산하지 않는다.
    rating: Mapped[float] = mapped_column(Float, nullable=False, comment='평점')
    rating_count: Mapped[int] = mapped_column(Integer, nullable=False, comment='평점 수')
    delivery_time: Mapped[int] = mapped_column(Integer, nullable=False, comment='배달 시간')
    delivery_fee: Mapped[int] = mapped_column(Integer, nullable=False, comment='배달비')

    # 어드민을 제작하면 detail 보다는 description 이 맞고, varchar 보다는 Text 타입이 맞다.
    detail: Mapped[str] = mapped_column(String(512), nullable=False, comment='가게 설명')
    tags: Mapped[list[Tag]] = relationship(Tag, secondary=RestaurantTag, uselist=True)

    __table_args__ = (
        {'comment': '레스토랑'},
    )


"""
{
  "tags": [
    "신규",
    "세일중"
  ],
"""

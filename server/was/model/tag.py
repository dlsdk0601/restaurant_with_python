from sqlalchemy import String, Column, Integer, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column

from was.model import Model, Base


class Tag(Model):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='PK')
    name: Mapped[str] = mapped_column(String(16), nullable=False, comment='태그 이름')


RestaurantTag = Table(
    'restaurant_tag', Base.metadata,
    Column('pk', Integer, autoincrement=True, primary_key=True, comment='PK'),
    Column('restaurant_pk', Integer, ForeignKey('restaurant.pk'), nullable=False, comment='restaurant - PK'),
    Column('tag_pk', Integer, ForeignKey('tag.pk'), nullable=False, comment='tag - PK'),
    comment='레스토랑 태그'
)

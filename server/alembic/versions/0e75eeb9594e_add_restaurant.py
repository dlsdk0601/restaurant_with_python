"""add_restaurant

Revision ID: 0e75eeb9594e
Revises: bba8f1c14dd4
Create Date: 2024-05-17 16:37:25.288555

"""
from enum import auto
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from ex.py.enum_ex import StringEnum

# revision identifiers, used by Alembic.
revision: str = '0e75eeb9594e'
down_revision: Union[str, None] = 'bba8f1c14dd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class RestaurantPriceRange(StringEnum):
    cheap = auto()
    medium = auto()
    expensive = auto()


restaurant_price_range = postgresql.ENUM(RestaurantPriceRange, create_type=False, name='restaurantpricerange')


def upgrade() -> None:
    restaurant_price_range.create(op.get_bind())
    op.create_table('restaurant',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False, comment='PK'),
                    sa.Column('name', sa.String(length=64), nullable=False, comment='레스토랑 이름'),
                    sa.Column('main_image_pk', sa.Integer(), nullable=False, comment='ASSET - FK'),
                    sa.Column('price_range', restaurant_price_range, nullable=False, comment='가격 수준'),
                    sa.Column('rating', sa.Float(), nullable=False, comment='평점'),
                    sa.Column('rating_count', sa.Integer(), nullable=False, comment='평점 수'),
                    sa.Column('delivery_time', sa.Integer(), nullable=False, comment='배달 시간'),
                    sa.Column('delivery_fee', sa.Integer(), nullable=False, comment='배달비'),
                    sa.Column('detail', sa.String(length=512), nullable=False, comment='가게 설명'),
                    sa.ForeignKeyConstraint(['main_image_pk'], ['asset.pk'], ),
                    sa.PrimaryKeyConstraint('pk')
                    )


def downgrade() -> None:
    op.drop_table('restaurant')
    restaurant_price_range.drop(op.get_bind())

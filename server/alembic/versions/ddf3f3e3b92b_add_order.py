"""add_order

Revision ID: ddf3f3e3b92b
Revises: 954d0ec4de55
Create Date: 2024-05-28 22:07:07.658353

"""
from enum import auto
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from ex.py.enum_ex import StringEnum

# revision identifiers, used by Alembic.
revision: str = 'ddf3f3e3b92b'
down_revision: Union[str, None] = '954d0ec4de55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class OrderState(StringEnum):
    INIT = auto()
    SUCCESS = auto()
    FAIL = auto()


order_state = postgresql.ENUM(OrderState, create_type=False, name='orderstate')


def upgrade() -> None:
    order_state.create(op.get_bind())
    op.create_table('order',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False, comment='PK'),
                    sa.Column('create_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.Column('state', order_state, nullable=False,
                              comment='상태'),
                    sa.Column('user_pk', sa.Integer(), nullable=False, comment='USER - FK'),
                    sa.Column('total_price', sa.Integer(), nullable=False, comment='주문 가격'),
                    sa.ForeignKeyConstraint(['user_pk'], ['user.pk'], ),
                    sa.PrimaryKeyConstraint('pk'),
                    comment='주문'
                    )
    op.create_table('order_item',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False, comment='PK'),
                    sa.Column('order_pk', sa.Integer(), nullable=False, comment='ORDER - FK'),
                    sa.Column('product_pk', sa.Integer(), nullable=False, comment='PRODUCT - FK'),
                    sa.Column('count', sa.Integer(), nullable=False, comment='갯수'),
                    sa.Column('price', sa.Integer(), nullable=False, comment='제품 가격'),
                    sa.ForeignKeyConstraint(['order_pk'], ['order.pk'], ),
                    sa.ForeignKeyConstraint(['product_pk'], ['product.pk'], ),
                    sa.PrimaryKeyConstraint('pk'),
                    comment='주문 상품'
                    )


def downgrade() -> None:
    op.drop_table('order_item')
    op.drop_table('order')
    order_state.drop(op.get_bind())

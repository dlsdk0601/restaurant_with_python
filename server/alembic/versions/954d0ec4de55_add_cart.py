"""add_cart

Revision ID: 954d0ec4de55
Revises: ea9dfda5096e
Create Date: 2024-05-25 22:07:42.100860

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '954d0ec4de55'
down_revision: Union[str, None] = 'ea9dfda5096e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('cart',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False, comment='PK'),
                    sa.Column('user_pk', sa.Integer(), nullable=False, comment='USER - FK'),
                    sa.ForeignKeyConstraint(['user_pk'], ['user.pk'], ),
                    sa.PrimaryKeyConstraint('pk'),
                    comment='장바구니'
                    )
    op.create_table('cart_item',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False, comment='PK'),
                    sa.Column('cart_pk', sa.Integer(), nullable=False, comment='CART - FK'),
                    sa.Column('product_pk', sa.Integer(), nullable=False, comment='PRODUCT - FK'),
                    sa.Column('count', sa.Integer(), nullable=False, comment='갯수'),
                    sa.Column('create_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.Column('update_at', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('delete_at', sa.DateTime(timezone=True), nullable=True),
                    sa.ForeignKeyConstraint(['cart_pk'], ['cart.pk'], ),
                    sa.ForeignKeyConstraint(['product_pk'], ['product.pk'], ),
                    sa.PrimaryKeyConstraint('pk'),
                    comment='장바구니 아이템'
                    )


def downgrade() -> None:
    op.drop_table('cart_item')
    op.drop_table('cart')

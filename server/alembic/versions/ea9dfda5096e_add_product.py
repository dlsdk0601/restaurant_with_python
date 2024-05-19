"""add_product

Revision ID: ea9dfda5096e
Revises: 505f85915cea
Create Date: 2024-05-19 22:37:58.267976

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ea9dfda5096e'
down_revision: Union[str, None] = '505f85915cea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('product',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False, comment='PK'),
                    sa.Column('name', sa.String(length=64), nullable=False, comment='제품 이름'),
                    sa.Column('main_image_pk', sa.Integer(), nullable=False, comment='ASSET - FK'),
                    sa.Column('detail', sa.String(length=512), nullable=False, comment='제품 설명'),
                    sa.Column('price', sa.Integer(), nullable=False, comment='가격'),
                    sa.Column('restaurant_pk', sa.Integer(), nullable=False, comment='레스토랑 - FK'),
                    sa.ForeignKeyConstraint(['main_image_pk'], ['asset.pk'], ),
                    sa.ForeignKeyConstraint(['restaurant_pk'], ['restaurant.pk'], ),
                    sa.PrimaryKeyConstraint('pk'),
                    comment='제품'
                    )


def downgrade() -> None:
    op.drop_table('product')

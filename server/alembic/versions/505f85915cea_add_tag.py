"""add_tag

Revision ID: 505f85915cea
Revises: 0e75eeb9594e
Create Date: 2024-05-17 16:51:25.894067

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '505f85915cea'
down_revision: Union[str, None] = '0e75eeb9594e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('tag',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False, comment='PK'),
                    sa.Column('name', sa.String(length=16), nullable=False, comment='태그 이름'),
                    sa.PrimaryKeyConstraint('pk')
                    )
    op.create_table('restaurant_tag',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False, comment='PK'),
                    sa.Column('restaurant_pk', sa.Integer(), nullable=False, comment='restaurant - PK'),
                    sa.Column('tag_pk', sa.Integer(), nullable=False, comment='tag - PK'),
                    sa.ForeignKeyConstraint(['restaurant_pk'], ['restaurant.pk'], ),
                    sa.ForeignKeyConstraint(['tag_pk'], ['tag.pk'], ),
                    sa.PrimaryKeyConstraint('pk'),
                    comment='레스토랑 태그'
                    )
    op.create_table_comment(
        'restaurant',
        '레스토랑',
        existing_comment=None,
        schema=None
    )


def downgrade() -> None:
    op.drop_table_comment(
        'restaurant',
        existing_comment='레스토랑',
        schema=None
    )
    op.drop_table('restaurant_tag')
    op.drop_table('tag')

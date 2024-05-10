"""add_asset

Revision ID: 9a241d64763b
Revises: fc55fb12b735
Create Date: 2024-05-10 19:18:03.043515

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9a241d64763b'
down_revision: Union[str, None] = 'fc55fb12b735'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('asset',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(length=64), nullable=False, comment='파일명'),
                    sa.Column('content_type', sa.String(length=128), nullable=False, comment='미디어 종류 - ex) image/gif'),
                    sa.Column('uuid', sa.UUID(), nullable=False, comment='고유키'),
                    sa.Column('url', sa.String(length=256), nullable=False, comment='웹 경로'),
                    sa.Column('download_url', sa.String(length=256), nullable=False, comment='다운로드 경로'),
                    sa.PrimaryKeyConstraint('pk'),
                    sa.UniqueConstraint('uuid'),
                    comment='업로드 파일'
                    )
    op.add_column('user', sa.Column('image_pk', sa.Integer(), nullable=False, comment='ASSET - FK'))
    op.create_foreign_key('user_image_pk_fkey', 'user', 'asset', ['image_pk'], ['pk'])


def downgrade() -> None:
    op.drop_constraint('user_image_pk_fkey', 'user', type_='foreignkey')
    op.drop_column('user', 'image_pk')
    op.drop_table('asset')

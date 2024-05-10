"""add_asset_user

Revision ID: bba8f1c14dd4
Revises: 
Create Date: 2024-05-10 23:31:56.524904

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'bba8f1c14dd4'
down_revision: Union[str, None] = None
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
    op.create_table('user',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False, comment='PK'),
                    sa.Column('email', sa.String(length=128), nullable=False, comment='email'),
                    sa.Column('password', sa.String(length=128), nullable=False, comment='암호화 비밀번호'),
                    sa.Column('name', sa.String(length=16), nullable=False, comment='이름'),
                    sa.Column('image_pk', sa.Integer(), nullable=False, comment='ASSET - FK'),
                    sa.ForeignKeyConstraint(['image_pk'], ['asset.pk'], ),
                    sa.PrimaryKeyConstraint('pk'),
                    sa.UniqueConstraint('email'),
                    comment='유저'
                    )
    op.create_table('user_authentication',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False, comment='PK'),
                    sa.Column('user_pk', sa.Integer(), nullable=False, comment='USER FK'),
                    sa.Column('access_token', sa.UUID(), nullable=False, comment='토큰'),
                    sa.Column('sign_out', sa.Boolean(), nullable=False, comment='로그아웃 여부'),
                    sa.Column('expire_at', sa.DateTime(timezone=True), nullable=False),
                    sa.Column('create_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.Column('update_at', sa.DateTime(timezone=True), nullable=True),
                    sa.ForeignKeyConstraint(['user_pk'], ['user.pk'], ),
                    sa.PrimaryKeyConstraint('pk'),
                    comment='Authentication'
                    )


def downgrade() -> None:
    op.drop_table('user_authentication')
    op.drop_table('user')
    op.drop_table('asset')

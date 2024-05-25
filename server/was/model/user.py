from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ex.py.datetime_ex import now
from ex.py.hash_ex import hash_password
from was import config
from was.model import Model
from was.model.asset import Asset

if TYPE_CHECKING:
    from was.model.cart import Cart


class User(Model):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='PK')
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, comment='email')
    password: Mapped[str] = mapped_column(String(128), nullable=False, comment='암호화 비밀번호')
    name: Mapped[str] = mapped_column(String(16), nullable=False, comment='이름')

    image_pk: Mapped[int] = mapped_column(ForeignKey(Asset.pk), nullable=False, comment='ASSET - FK')
    image: Mapped[Asset] = relationship()

    cart: Mapped['Cart'] = relationship('Cart', back_populates='cart')

    @staticmethod
    def hash_password(password: str) -> str:
        return hash_password(config.SECRET_PASSWORD_BASE_SALT, password)

    __table_args__ = (
        {'comment': '유저'},
    )


class UserAuthentication(Model):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='PK')
    user_pk: Mapped[int] = mapped_column(ForeignKey(User.pk), nullable=False, comment='USER FK')
    user: Mapped['User'] = relationship()
    access_token: Mapped[UUID] = mapped_column(postgresql.UUID(), nullable=False, comment='토큰')
    sign_out: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment='로그아웃 여부')
    expire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now(), default=None)

    def update_expire_at(self) -> None:
        # 일주일 동안 사용가능
        # noinspection PyTypeChecker
        self.expire_at = now() + timedelta(days=7)

    @hybrid_property
    def expired(self) -> bool:
        return now() > self.expire_at

    __table_args__ = (
        {'comment': 'Authentication'},
    )

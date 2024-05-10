from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# from ex.sqlalchemy_ex import BaseQueryEx

db: SQLAlchemy = SQLAlchemy(
    # query_class=BaseQueryEx,
    session_options={"autoflush": False}
)
# https://github.com/sqlalchemy/sqlalchemy2-stubs/issues/54
# Base 만 올바르게 찾기 때문에, 기본 type 지정으로 미리한다.
Base = DeclarativeBase
Base = db.Model  # type: ignore


class Model(Base):
    # if TYPE_CHECKING:
    #     from mypy.typeshed.stdlib.typing_extensions import Self
    # query: BaseQueryEx['Self']

    __abstract__ = True


LOCK_ASSET = 1

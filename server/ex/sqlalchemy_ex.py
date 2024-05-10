from itertools import count
from typing import TypeVar, Generic, List, Union, Tuple, Callable

from sqlalchemy.sql.selectable import Select
from flask_sqlalchemy.session import Session
from sqlalchemy import func, or_, and_, text, Index
from sqlalchemy.orm import scoped_session
# user.deleted_at == None 을 별로 좋아하지 않는다.
# user.deleted_at == null
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql.elements import BooleanClauseList

from ex.api import BaseModel, GenericModel
from was.model import db

null: None = None
true: bool = True
false: bool = False


def int_ceil(x: int, y: int) -> int:
    """
    equivalent to math.ceil(x / y)
    :param x:
    :param y:
    :return:
    """
    q, r = divmod(x, y)
    if r:
        q += 1
    return q


T = TypeVar('T')
U = TypeVar('U')

PAGE_ROW_ITEM = TypeVar('PAGE_ROW_ITEM', bound=BaseModel)
TableArgs = Tuple[Index | dict[str, str], ...]


class PageRow(GenericModel, Generic[PAGE_ROW_ITEM]):
    no: int
    item: PAGE_ROW_ITEM


class Pagination(GenericModel, Generic[PAGE_ROW_ITEM]):
    page: int
    pages: List[int]
    prev_page: int
    next_page: int
    has_prev: bool
    has_next: bool
    total: int
    rows: List[PageRow[PAGE_ROW_ITEM]]


# OPT :: per_nav ?
def api_paginate(q: Select, page, map_: Callable[[T], PAGE_ROW_ITEM], per_page=10) -> 'Pagination[PAGE_ROW_ITEM]':
    p = (db.paginate(q, page=page, per_page=per_page))
    total = p.total
    if total == 0 or total is None:
        last = 1
    else:
        last = int_ceil(total, per_page)
    first = max(p.page - 2, 1)
    pages = tuple(range(first, min(last, first + 5) + 1))
    start = (page - 1) * per_page
    items = tuple(map(map_, p.items))
    items_indexed = tuple(zip(count(total - start, step=-1), items))

    return Pagination(
        page=p.page,
        pages=list(pages),
        prev_page=max(p.page - 1, 1),
        next_page=min(p.page + 1, last),
        has_next=p.has_next,
        has_prev=p.has_prev,
        total=p.total,
        rows=[PageRow(no=index, item=item) for (index, item) in items_indexed]
    )


#
# class BaseQueryEx(BaseQuery, Generic[T]):
#     def api_pagination(self: Query, page, map_: Callable[[T], PAGE_ROW_ITEM], per_page=10, per_nav=10,
#                        base: paginatify_sqlalchemy.NavigationBase = paginatify_sqlalchemy.NavigationBase.STANDARD,
#                        ) -> 'Pagination[PAGE_ROW_ITEM]':
#         p: paginatify_sqlalchemy.Pagination[PAGE_ROW_ITEM] = paginatify_sqlalchemy \
#             .paginatify(query=self, page=page, per_page=per_page, per_nav=per_nav, base=base, map_=map_)
#         return Pagination(
#             page=p.page,
#             pages=list(p.pages),
#             prev_page=p.prev,
#             next_page=p.next,
#             has_next=p.has_next,
#             has_prev=p.has_prev,
#             total=p.total,
#             rows=[PageRow(no=index, item=item) for (index, item) in
#                   p.items_indexed]
#         )  # type: ignore
#
#     def one_or_404(self):
#         return self.one_or_none() or abort(404)
#
#     def first_or_none(self):
#         return self.limit(1).one_or_none()
#
#     def pagination(self, page=1, per_page=10, per_nav=10, map_=lambda x: x):
#         return paginatify_sqlalchemy.paginatify(self, page=page if page else 1, per_page=per_page if per_page else 10,
#                                                 per_nav=per_nav, map_=map_)


# https://github.com/sqlalchemy/sqlalchemy/issues/3482
def icontains(column, string: str):
    return func.lower(column).contains(string.lower(), autoescape=True)


def isearch(string: str, *columns):
    keywords = list(filter(bool, map(lambda x: x.strip(), string.split(' '))))

    conditions = []

    for column in columns:
        and_conditions = [icontains(column, keyword) for keyword in keywords]
        conditions.append(and_(True, *and_conditions))

    return or_(*conditions)


def pg_xlock2(session: Session | scoped_session[Session], group_id: int, lock_id: int) -> None:
    session.execute(
        text('select pg_advisory_xact_lock(:group_id, :lock_id)'),
        {'group_id': group_id, 'lock_id': lock_id}
    )


def pg_try_xlock2(session: Session | scoped_session[Session], group_id: int, lock_id: int) -> bool:
    return session.scalar(
        text('select pg_try_advisory_xact_lock(:group_id, :lock_id)'),
        {'group_id': group_id, 'lock_id': lock_id}
    )


Condition = Union[ColumnElement[bool], BooleanClauseList]
Conditions = List[Condition]

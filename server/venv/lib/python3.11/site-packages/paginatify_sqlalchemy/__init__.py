from typing import TypeVar, Callable

from sqlalchemy.orm import Query

from paginatify import NavigationBase, Pagination, paginatify as _paginatify

T = TypeVar('T')
U = TypeVar('U')


def paginatify(query: Query, page=1, per_page=10, per_nav=10, base: NavigationBase = NavigationBase.STANDARD,
               map_: Callable[[T], U] = lambda x: x) -> Pagination[U]:
    return _paginatify(query, page, per_page, per_nav, base, map_, query.order_by(None).count)

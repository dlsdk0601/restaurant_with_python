from dataclasses import dataclass
from enum import Enum, auto
from itertools import count
from typing import Tuple, TypeVar, Generic, Callable, Sequence


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


@dataclass
class Pagination(Generic[T]):
    total: int

    first: int
    last: int

    page: int

    prev: int
    next: int
    has_prev: bool
    has_next: bool

    pages: Tuple[int]
    nav_head: int
    nav_tail: int
    nav_prev: int
    nav_next: int
    has_prev: bool
    has_next: bool
    has_nav_prev: bool
    has_nav_next: bool

    items: Tuple[T]
    items_indexed: Tuple[(int, T)]


class NavigationBase(Enum):
    STANDARD = auto()
    CENTER = auto()


def paginatify(query: Sequence[T], page=1, per_page=10, per_nav=10, base: NavigationBase = NavigationBase.STANDARD,
               map_: Callable[[T], U] = lambda x: x, total_count_query: Callable[[], int] = None) -> Pagination[U]:
    first = 1
    total = total_count_query() if total_count_query else len(query)
    if total == 0:
        last = 1
    else:
        last = int_ceil(total, per_page)
    page = max(min(last, page), 1)

    prev = max(page - 1, 1)
    has_prev = prev != page
    next_ = min(page + 1, last)
    has_next = next_ != page

    if base == NavigationBase.STANDARD:
        nav_head = per_nav * (int_ceil(page, per_nav) - 1) + 1
    else:
        nav_head = max(first, page - ((per_nav - 1) // 2))

    nav_tail = min(last, nav_head + per_nav - 1)
    nav_prev = max(page - per_nav, 1)
    has_nav_prev = nav_prev < nav_head
    nav_next = min(page + per_nav, last)
    has_nav_next = nav_next > nav_tail

    pages = tuple(range(nav_head, nav_tail + 1))

    start = (page - 1) * per_page
    items = tuple(map(map_, query[start: min(total, start + per_page)]))
    items_indexed = tuple(zip(count(total - start, step=-1), items))

    return Pagination(
        total=total, first=first, last=last, page=page, prev=prev, next=next_, has_prev=has_prev, has_next=has_next,
        pages=pages, nav_head=nav_head, nav_tail=nav_tail, nav_prev=nav_prev, nav_next=nav_next,
        has_nav_prev=has_nav_prev, has_nav_next=has_nav_next,
        items=items, items_indexed=items_indexed
    )

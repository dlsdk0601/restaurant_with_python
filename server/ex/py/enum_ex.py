from collections import defaultdict
from enum import Enum, auto, unique
from typing import Dict, TypeVar, Optional, Callable, Set, TYPE_CHECKING

from more_itertools import first

if TYPE_CHECKING:
    from mypy.typeshed.stdlib.typing_extensions import Self


class LabelEnum(Enum):
    """사용자 친화적인 Enum 이름

    >>> class Color(StringEnum):
    ...    RED = auto()
    ...    GREEN = auto()
    ...    BLUE = auto()
    ...    __label__ = {'admin': {RED: '빨강', GREEN: '초록'}, 'api' : {GREEN: 'Green'}}
    >>> Color.RED
    <Color.RED: 'RED'>
    >>> dict(Color.GREEN.label)
    {'admin': '초록', 'api': 'Green'}
    >>> Color.RED.label['admin']
    '빨강'
    >>> Color.RED.label['api']
    'RED'
    >>> Color.BLUE.label['admin']
    'BLUE'
    """

    @property
    def label(self) -> Dict[str, str]:
        if not hasattr(self, '__labeled__'):
            sections = getattr(type(self), '__label__', {})

            labeled = defaultdict(lambda: self.name)
            for section, labels in sections.items():
                if label := labels.get(self.name):
                    labeled[section] = label
            setattr(self, '__labeled__', labeled)

        return getattr(self, '__labeled__')


T = TypeVar('T')
U = TypeVar('U')


def enum_from_value(cons: Callable[[U], T], value: U) -> Optional[T]:
    try:
        return cons(value)
    except ValueError:
        return None


@unique
class StringEnum(str, LabelEnum):
    """숫자 대신 필드명을 사용한다

    >>> class Color(StringEnum):
    ...    RED = auto()
    ...    GREEN = auto()
    ...    BLUE = auto()
    ...
    >>> Color.RED
    <Color.RED: 'RED'>
    >>> Color.RED.value
    'RED'
    >>> str(Color.RED)
    'RED'
    """

    # Enum 클래스의 메소드 정의가 다음과 같다.
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        """wtforms 에서는 항상 str(value) 로 값을 사용한다.
        """
        return self.value


class State(StringEnum):
    @classmethod
    def transitions(cls: 'Self') -> Dict['Self', Set['Self']]:
        return {}

    def can_transit(self, next_state: 'Self') -> bool:
        if self == next_state:
            return True

        transitions = self.__class__.transitions()
        return next_state in transitions.get(self, set())

    def validate_transition(self, next_state: 'Self') -> Optional[str]:
        if self.can_transit(next_state):
            return None

        return f'{self}에서 {next_state}로는 변경할 수 없습니다.'

    def validate_terminal(self) -> Optional[str]:
        # 상태 변경이 존재하면, 계속 변경할 수 있다.
        if self.transitions().get(self, set()):
            return None

        return f'{self}에서는 수정할 수 없습니다.'

    def validate(self, is_initial: bool, next_state: 'Self') -> Optional[str]:
        if is_initial:
            initial = first(type(self).transitions().keys(), None)
            if self != initial:
                return f'잘못된 {self} 상태입니다. 생성 시에는 반드시 {initial} 상태이어야 합니다.'
            if next_state != initial:
                return f'잘못된 {next_state} 상태 요청입니다. 생성 시에는 반드시 {initial} 상태이어야 합니다.'
        return self.validate_terminal() or self.validate_transition(next_state)

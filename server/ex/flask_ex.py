import logging
import pkgutil
import sys
from types import ModuleType
from typing import Optional, Tuple, Union, Type, TypeVar, cast

from flask import Flask, g, abort, request
# werkzeug 는 flask 에 포함되어 있다.
# noinspection PyPackageRequirements
from werkzeug.local import LocalProxy


def initialize(app: Flask) -> None:
    """
    일반적인 초기화
    :param app:
    """
    # 로거 기본값 설정
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    if app.debug:
        _initialize_debug(app)


def _initialize_debug(app: Flask):
    # static 리소스가 개발중에는 캐슁 되지 않도록 변경
    if not app.config.get('SEND_FILE_MAX_AGE_DEFAULT'):
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # 별다른 설정이 없을 경우 env 는 개발로 정의한다.
    if app.config['ENV'] == 'production':
        app.config['ENV'] = 'development'


# OPTS :: blueprints 타입 수정, ModuleType + (object.app: Blueprint)
def register_blueprints(app: Flask, *blueprints: Union[ModuleType, Tuple[ModuleType, str]]) -> None:
    """blueprint 모듈 전체를 로딩하고, app 에 url_prefix 와 함께 등록하여 준다.
    """
    url_prefix: Optional[str]

    for bp in blueprints:
        if isinstance(bp, tuple):
            module, url_prefix = bp
        else:
            module, url_prefix = bp, None

        load_submodules(module)

        app.register_blueprint(
            blueprint=module.app,  # type: ignore
            url_prefix=url_prefix
        )


def load_submodules(module) -> None:
    # OPT :: ignore find_module type check, 너무 상황이 복잡하니 나중에 다시 확인 한다.
    for finder, name, is_pkg in pkgutil.iter_modules(module.__path__):
        module_name = f"{module.__name__}.{name}"
        if module_name not in sys.modules:
            child_module = finder.find_module(module_name).load_module()  # type: ignore
        else:
            child_module = sys.modules[module_name]

        if is_pkg:
            load_submodules(child_module)


T = TypeVar('T')


def global_proxy(name: str, builder: Type[T]) -> T:
    def f():
        if not hasattr(g, name):
            setattr(g, name, builder())
        return getattr(g, name)

    # https://github.com/python/mypy/issues/7347
    return LocalProxy(f)  # type: ignore


def not_found():
    abort(404)


is_get = cast(bool, LocalProxy(lambda: request.method == 'GET'))
is_post = cast(bool, LocalProxy(lambda: request.method == 'POST'))

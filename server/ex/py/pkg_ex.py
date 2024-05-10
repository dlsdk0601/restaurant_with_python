import pkgutil
import sys
from typing import Any, List


def find_global_values(module: Any) -> List[Any]:
    # OPT :: ignore find_module type check, 너무 상황이 복잡하니 나중에 다시 확인 한다.

    re: List[Any] = list(module.__dict__.values())
    for finder, name, is_pkg in pkgutil.iter_modules(module.__path__):
        module_name = f"{module.__name__}.{name}"
        if module_name not in sys.modules:
            child_module = finder.find_module(module_name).load_module()  # type: ignore
        else:
            child_module = sys.modules[module_name]

        if is_pkg:
            child_re = find_global_values(child_module)
            re.extend(child_re)
        else:
            re.extend(child_module.__dict__.values())

    return re

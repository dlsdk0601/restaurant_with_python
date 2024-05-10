import hashlib
import shutil
from pathlib import Path

from was import config

BUILD_PATH = config.was_root_path.parent / 'xsailr-app' / 'build' / 'web'


def main() -> None:
    assert BUILD_PATH.exists(), f'Build path not found: {BUILD_PATH}'

    # patch main.dart.js
    main_dart_path = _hash_file(BUILD_PATH / 'main.dart.js')

    # patch flutter.js
    flutter_path = _hash_file(BUILD_PATH / 'flutter.js')
    _replace_file_name_in_file(flutter_path, 'main.dart.js', main_dart_path.name)

    # TODO 이려면 여러번 실행할 수 없다.
    # patch index.html
    index_path = BUILD_PATH / 'index.html'
    _replace_file_name_in_file(index_path, 'flutter.js', flutter_path.name)
    # patch flutter_service_worker.js
    flutter_service_worker_path = BUILD_PATH / 'flutter_service_worker.js'
    _replace_file_name_in_file(flutter_service_worker_path, 'main.dart.js', main_dart_path.name)
    _replace_file_name_in_file(flutter_service_worker_path, 'flutter.js', flutter_path.name)


def _hash_file(file_path: Path) -> Path:
    with file_path.open('rb') as f:
        # noinspection PyTypeChecker
        md5 = hashlib.file_digest(f, 'md5').hexdigest()
    hashed_file_path = file_path.parent / f'{file_path.stem}.{md5}{file_path.suffix}'
    shutil.copy(file_path, hashed_file_path)
    return hashed_file_path


def _replace_file_name_in_file(file_path: Path, old_file_name: str, new_file_name: str) -> None:
    with file_path.open('r') as f:
        content = f.read()
    content = content.replace(old_file_name, new_file_name)
    with file_path.open('w') as f:
        f.write(content)


if __name__ == '__main__':
    main()

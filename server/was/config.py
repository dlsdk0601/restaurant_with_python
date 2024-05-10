from os import environ
from pathlib import Path

from sconfig import configure

PORT = 5001
DEBUG = False
SECRET_KEY = '30d3ce2d112b78ca50ad16ca4448d9188856a912b57a677efb9e349b8c863263'
SECRET_PASSWORD_BASE_SALT = SECRET_KEY

# 파일 업로드 제한
FILE_UPLOAD_MAX_SIZE = 100 * 1024 * 1024

# DB -> 한글 정렬을 위해 남겨두는데 프로젝트 기본으로 설정해두고 사용할 경우 대비해준다.
DB_COLLNAME = 'und-x-icu'

# Flask-SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = environ.get(
    'DATABASE_URL',
    f'postgres://postgres@{environ.get("DOCKER_HOST", "localhost")}:30311/restaurant'
)
SQLALCHEMY_ECHO = False

configure(__name__)

# SALT 는 Bytes 타입이어야 한다.
SECRET_PASSWORD_BASE_SALT = bytes.fromhex(SECRET_PASSWORD_BASE_SALT)

# https://docs.sqlalchemy.org/en/14/changelog/changelog_14.html#change-3687655465c25a39b968b4f5f6e9170b
# postgres 단축 이름을 더이상 지원하지 않는다.
if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + SQLALCHEMY_DATABASE_URI.removeprefix('postgres://')

was_root_path: Path = Path(__file__).resolve().parent.parent
was_tmp_path: Path = was_root_path / "tmp"

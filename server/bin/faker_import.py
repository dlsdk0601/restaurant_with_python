import mimetypes
import os
from pathlib import Path
from typing import Callable

from faker import Faker

from ex.faker_ex import faker_unique, faker_call
from was.application import app
from was.model import db
from was.model.asset import Asset
from was.model.user import User

static_images_path = (Path(__file__).parent.parent / 'was' / 'static' / 'assets' / 'images').resolve()


def main() -> None:
    importers: list[Callable[[Faker], None]] = [
        _import_asset,
        _import_user,
    ]

    for importer in importers:
        _users.clear()
        with app.app_context():
            print(f'import {importer.__name__.removeprefix("_import_")} ... ', flush=True, end='')
            faker = Faker('ko_KR')
            faker.seed_instance(importer.__name__)
            importer(faker)
            print(f'done')


def _import_asset(faker: Faker) -> None:
    assets: list[Asset] = []
    directories = os.listdir(static_images_path)
    for directory in directories:
        dir_path = os.path.join(static_images_path, directory)
        files = os.listdir(dir_path)
        for file in files:
            file_path = os.path.join(dir_path, file)
            content_type, _ = mimetypes.guess_type(file_path)
            asset = Asset.new_(name=file, content_type=content_type)
            assets.append(asset)

    db.session.add_all(assets)
    db.session.commit()


def _import_user(faker: Faker) -> None:
    emails: set[str] = set()

    def new_user():
        email = faker_unique(faker.email, emails)
        name = faker.name()
        user = User(email=email)
        user.name = name
        user.password = User.hash_password(name)
        user.image_pk = 35  # faker 니까 하드코딩으로 박자

        return user

    users = faker_call(faker, new_user, 13)

    # test 계정
    users[0].email = 'test'
    users[0].password = '1234'
    db.session.add_all(users)
    db.session.commit()


_users: list[User] = []


def fetch_users():
    global _users
    if not _users:
        _users = [x for x in db.session.execute(db.select(User).order_by(User.pk)).scalars()]
    return _users


def fetch_user(faker: Faker):
    return faker.random_element(fetch_users())


_user_pks: list[int] = []


def fetch_user_pks():
    global _user_pks
    if not _user_pks:
        _user_pks = [x.pk for x in db.session.execute(db.select(User)).scalars()]
    return _user_pks


def fetch_user_pk(faker: Faker):
    return faker.random_element(fetch_user_pks())


if __name__ == '__main__':
    main()

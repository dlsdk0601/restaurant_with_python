import mimetypes
import os
from collections import OrderedDict
from typing import Callable

from faker import Faker

from ex.faker_ex import faker_unique, faker_call
from was.application import app
from was.config import static_images_path
from was.model import db
from was.model.asset import Asset
from was.model.restaurant import Restaurant, RestaurantPriceRange
from was.model.tag import Tag
from was.model.user import User


def main() -> None:
    importers: list[Callable[[Faker], None]] = [
        _import_asset,
        _import_user,
        _import_tag,
        _import_restaurant,
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


def _import_restaurant(faker: Faker) -> None:
    names: set[str] = set()

    def new_restaurant():
        name = faker_unique(faker.company, names)
        price_range = faker.random_element(OrderedDict([
            (RestaurantPriceRange.cheap, 0.3),
            (RestaurantPriceRange.medium, 0.3),
            (RestaurantPriceRange.expensive, 0.4),
        ]))
        restaurant = Restaurant(
            name=name, price_range=price_range, rating=faker.pyfloat(left_digits=1, right_digits=2, positive=True),
            rating_count=faker.random_int(min=0, max=100), delivery_time=faker.random_int(min=10, max=40),
            delivery_fee=faker.random_int(min=0, max=3000), detail=faker.paragraph(nb_sentences=5),
            main_image_pk=fetch_asset_pk(faker)
        )

        tags: set[Tag] = set()
        for _ in range(10):
            tags.add(fetch_tag(faker))
        restaurant.tags = list(tags)

        return restaurant

    restaurants = faker_call(faker, new_restaurant, 73)
    db.session.add_all(restaurants)
    db.session.commit()


def _import_tag(faker: Faker) -> None:
    names: set[str] = set()

    def new_tag():
        name = faker_unique(faker.word, names)
        tag = Tag(name=name)
        return tag

    tags = faker_call(faker, new_tag, 200)

    db.session.add_all(tags)
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


_asset_pks: list[int] = []


def fetch_asset_pks():
    global _asset_pks
    if not _asset_pks:
        _asset_pks = [x.pk for x in db.session.execute(db.select(Asset)).scalars()]

    return _asset_pks


def fetch_asset_pk(faker: Faker):
    return faker.random_element(fetch_asset_pks())


_restaurant_pks: list[int] = []


def fetch_restaurant_pks():
    global _restaurant_pks
    if not _restaurant_pks:
        _restaurant_pks = [x.pk for x in db.session.execute(db.select(Restaurant)).scalars()]
    return _restaurant_pks


def fetch_restaurant_pk(faker: Faker):
    return faker.random_element(fetch_restaurant_pks())


_tag_pks: list[int] = []


def fetch_tag_pks():
    global _tag_pks
    if not _tag_pks:
        _tag_pks = [x.pk for x in db.session.execute(db.select(Tag)).scalars()]
    return _tag_pks


def fetch_tag_pk(faker: Faker):
    return faker.random_element(fetch_tag_pks())


_tags: list[Tag] = []


def fetch_tags():
    global _tags
    if not _tags:
        _tags = [x for x in db.session.execute(db.select(Tag)).scalars()]
    return _tags


def fetch_tag(faker: Faker):
    return faker.random_element(fetch_tags())


if __name__ == '__main__':
    main()

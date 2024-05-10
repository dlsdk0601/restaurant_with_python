from typing import Callable

from faker import Faker

from was.application import app
from was.model import db
from was.model.user import User


def main() -> None:
    importers: list[Callable[[Faker], None]] = [
        _import_user,
    ]

    for importer in importers:
        _users.clear()
        with app.app_context():
            print(f'import {importer.__name__.removeprefix("_import_")} ... ', flush=True, end='')
            faker = Faker()
            faker.seed_instance(importer.__name__)
            importer(faker)
            print(f'done')


def _import_user(faker: Faker) -> None:
    print('d')
    # user_ids: set[str] = set()
    #
    # def new_user():
    #     user_name = faker_unique(faker.user_name, user_ids)
    #     user_type = faker.random_element(OrderedDict([
    #         (UserType.DEV, 0.4),
    #         (UserType.APPLE, 0.3),
    #         (UserType.GOOGLE, 0.3),
    #     ]))
    #
    #     if user_type == UserType.GOOGLE:
    #         user = GoogleUser()
    #         user.sub = faker.uuid4()
    #         user.email = faker.email()
    #         user.social_name = user_name
    #     elif user_type == UserType.APPLE:
    #         user = AppleUser()
    #         user.sub = faker.uuid4()
    #         user.given_name = faker.user_name()
    #         user.family_name = user_name
    #     else:
    #         user = DevUser()
    #         user.email = f'{user_name}@dev.com'
    #         user.social_name = user_name
    #     user.type = user_type
    #
    #     user.name = user.social_name if faker.random_element((True, False)) else faker.user_name()
    #     user.profile_image = new_asset() if faker.random_element((True, False)) else None
    #
    #     space_travel = SpaceTravel.new_(user)
    #     space_travel.arrival_at = faker.random_element(OrderedDict([
    #         (now() + timedelta(days=7), 0.8),
    #         (None, 0.2),
    #     ]))
    #     space_travel.landing_at = faker.random_element(OrderedDict([
    #         (space_travel.arrival_at + timedelta(days=1), 0.8),
    #         (None, 0.2),
    #     ])) if space_travel.arrival_at is not None else None
    #
    #     db.session.add(space_travel)
    #
    #     if faker.random_element(OrderedDict([(True, 0.2), (False, 0.8)])):
    #         logbook = Logbook.new_(user, faker.sentence(nb_words=10))
    #         db.session.add(logbook)
    #
    #     space_ship_history = SpaceShipHistory.new_(user)
    #     db.session.add(space_ship_history)
    #
    #     return user
    #
    # users = faker_call(faker, new_user, 58)
    # db.session.add_all(users)
    # db.session.commit()


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

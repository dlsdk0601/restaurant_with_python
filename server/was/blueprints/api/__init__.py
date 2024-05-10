from typing import Tuple, Optional

from flask import request
from sqlalchemy.orm import joinedload

from ex.api import ApiBlueprint
from ex.flask_ex import global_proxy
from ex.py.ex import parse_uuid
from ex.sqlalchemy_ex import false
from was.model import db
from was.model.user import UserAuthentication, User


class _ApiBlueprint(ApiBlueprint[None]):
    def validate_login(self) -> bool:
        return bg.user is not None

    def validate_permission(self, permissions: Tuple[None, ...]) -> bool:
        # OPT :: 퍼미션이 필요할 경우 처리
        return True


app = _ApiBlueprint('api_app', __name__)


class UserGlobal:
    _user_authentication: UserAuthentication | None

    @property
    def user_authentication(self) -> Optional[UserAuthentication]:
        if hasattr(self, "_user_authentication"):
            return self._user_authentication
        self._user_authentication = None

        access_token = parse_uuid(request.headers.get("X-Access-Token"))
        if not access_token:
            return None

        authentication_query = db.select(UserAuthentication) \
            .options(joinedload(UserAuthentication.user)) \
            .filter(UserAuthentication.access_token == access_token,
                    ~UserAuthentication.expired,
                    UserAuthentication.sign_out == false)
        authentication: UserAuthentication | None = db.session.execute(authentication_query).scalar_one_or_none()
        if not authentication:
            return None

        authentication.update_expire_at()
        self._user_authentication = authentication
        return self._user_authentication

    @user_authentication.setter
    def user_authentication(self, authentication: UserAuthentication):
        self._user_authentication = authentication

    @property
    def user(self) -> Optional[User]:
        if not self.user_authentication:
            return None
        return self.user_authentication.user


bg = global_proxy("user", UserGlobal)

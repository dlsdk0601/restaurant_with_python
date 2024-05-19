from typing import Tuple, Optional
from uuid import UUID

from flask import request, session, Response
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from ex.api import ApiBlueprint, res_jsonify, Res, ResStatus
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
    _USER_AUTHENTICATION_PK = "USER_AUTHENTICATION_PK"
    _user_authentication: UserAuthentication | None

    def get_user_authentication_pk(self) -> int | None:
        return session.get(self._USER_AUTHENTICATION_PK)

    def set_user_authentication_pk(self, access_token_pk):
        session[self._USER_AUTHENTICATION_PK] = access_token_pk

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


@app.before_request
def before_request() -> Response | None:
    req_token = request.headers.get('X-Access-Token')
    auth: UserAuthentication | None = None
    access_token: UUID | None = None

    if req_token:
        try:
            access_token = UUID(req_token)
        except ValueError:
            pass

    if access_token:
        conditions = [
            UserAuthentication.access_token == access_token,
            UserAuthentication.expire_at >= func.now()
        ]
        auth = db.session.query(UserAuthentication).filter(*conditions).one_or_none()

        if auth:
            auth.update_expire_at()
            db.session.commit()

    if not auth:
        require_access_token = True
        match ((request.endpoint or '').split('.', maxsplit=2)):
            case [_, endpoint]:
                if endpoint in ['sign_in', 'asset_show']:
                    require_access_token = False
            case _:
                pass

        if require_access_token:
            return res_jsonify(Res(errors=[], status=ResStatus.INVALID_ACCESS_TOKEN, validation_errors=[]))

    return None

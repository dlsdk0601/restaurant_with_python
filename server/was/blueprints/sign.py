from uuid import UUID, uuid4

from sqlalchemy import func

from ex.api import BaseModel, Res, err, ok
from was.blueprints import app, bg
from was.model import db
from was.model.user import User, UserAuthentication


class SignInReq(BaseModel):
    id: str
    password: str


class SignInRes(BaseModel):
    access_token: UUID


@app.api(public=True)
def sign_in(req: SignInReq) -> Res[SignInRes]:
    user: User | None = db.session.execute(
        db.select(User).filter_by(email=req.id)
    ) \
        .scalar_one_or_none()

    if not user or user.password != User.hash_password(req.password):
        return err("잘못된 아이디 또는 암호입니다.")

    auth = UserAuthentication()
    auth.access_token = uuid4()
    auth.user = user
    auth.update_expire_at()
    db.session.add(auth)
    db.session.commit()

    bg.set_user_authentication_pk(access_token_pk=auth.pk)
    return ok(SignInRes(access_token=auth.access_token))


class SignOutReq(BaseModel):
    pass


class SignOutRes(BaseModel):
    pass


@app.api(public=True)
def sign_out(req: SignOutReq) -> Res[SignOutRes]:
    pk = bg.get_user_authentication_pk()

    if pk:
        bg.set_user_authentication_pk(None)
        token = db.session.execute(
            db.select(UserAuthentication).filter_by(pk=pk)
        ) \
            .scalar_one_or_none()
        if token:
            token.expire_at = func.now()
            db.session.commit()

    return ok(SignOutRes())

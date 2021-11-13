from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.app.dependencies import get_db
from src.schemas.user import UserLogin, UserBase
from src.database.crud import user as user_crud

router = APIRouter(prefix="/user", tags=["User"])
security = HTTPBearer()


@router.get("/", status_code=200)
async def get_user(session: Session = Depends(get_db),
                   Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return user_crud.get_user(int(Authorize.get_jwt_subject()), session)


@router.patch("/", status_code=200)
async def set_user(user_info: UserBase, session: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return user_crud.set_user(int(Authorize.get_jwt_subject()), user_info, session)


@router.delete("/", status_code=200)
async def delete_user(session: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return user_crud.delete_user(int(Authorize.get_jwt_subject()), session)


@router.post("/auth", status_code=200)
async def auth_user(form_data: UserLogin, session: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = user_crud.get_user_by_username(username=form_data.login, session=session)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect login or password')
    if not user_crud.validate_password(password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=400, detail='Incorrect login or password')
    return user_crud.create_user_token(user_id=user.id, session=session, Authorize=Authorize)


@router.post("/token", status_code=200)
async def refresh_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=user)
    return {"access_token": new_access_token}

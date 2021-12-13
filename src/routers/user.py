import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security, File
from fastapi.responses import Response, FileResponse
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.app.dependencies import get_db
from src.models.user import UserOut, UserUpdate, UserCreate
from src.models.general import UserToken
from src.repositories import user, avatar

router = APIRouter(prefix="/user", tags=["User"])
security = HTTPBearer()


@router.get("/curr", status_code=200, response_model=UserOut)
async def get_current_user(session: Session = Depends(get_db),
                   Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    curr_user = user.get_user_by_id(int(Authorize.get_jwt_subject()), session)
    if not curr_user:
        raise HTTPException(status_code=400, detail=[{'msg': 'User with this email does not exist'}])
    return curr_user


@router.get("/", status_code=200, response_model=UserOut)
async def get_user_by_id(id: int, session: Session = Depends(get_db)):
    curr_user = user.get_user_by_id(id, session)
    if not curr_user:
        raise HTTPException(status_code=400, detail=[{'msg': 'User with this id does not exist'}])
    return curr_user


@router.get("/all", status_code=200, response_model=List[UserOut])
async def get_all_user(limit: int = 100, skip: int = 0, session: Session = Depends(get_db)):
    return user.get_all_user(session, limit, skip)


@router.post("/", status_code=200, response_model=UserToken)
async def create_user(user_info: UserCreate, session: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    curr_user = user.create_user(u=user_info, s=session)
    if not curr_user:
        raise HTTPException(status_code=400, detail=[{'msg': 'User with this email already exists'}])
    token = user.create_user_token(curr_user.id, Authorize)
    return UserToken(User=curr_user, Token=token)


@router.patch("/", status_code=200, response_model=UserOut)
async def edit_current_user(user_info: UserUpdate, session: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    curr_user = user.edit_user(u=user_info, id=int(Authorize.get_jwt_subject()), s=session)
    if not curr_user:
        raise HTTPException(status_code=400, detail=[{'msg': 'Editing failed'}])
    return curr_user


@router.patch("/avatar", status_code=200, response_model=UserOut)
async def edit_current_user_avatar(image: bytes = File(...), session: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    mapper = avatar.create_avatar(file=image, s=session)
    return user.edit_avatar_id(user_id=int(Authorize.get_jwt_subject()), avatar_id=mapper.id, s=session)


@router.get("/avatar", status_code=200, response_model=UserOut)
async def get_avatar_by_user_id(user_id: int, session: Session = Depends(get_db)):
    curr_user = user.get_user_by_id(user_id, s=session)
    curr_avatar = avatar.get_avatar(curr_user.avatar_id, session)
    if curr_avatar is None:
        return FileResponse('src/avatars/user_default_avatar.png')
    return Response(content=curr_avatar.file, media_type='image/png')


@router.delete("/avatar", status_code=200, response_model=UserOut)
async def delete_current_user_avatar(session: Session = Depends(get_db),
                                     Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    curr_user = user.get_user_by_id(int(Authorize.get_jwt_subject()), s=session)
    curr_avatar = avatar.get_avatar(curr_user.avatar_id, session)
    if curr_avatar is None:
        raise HTTPException(status_code=400, detail=[{'msg': 'The user does not have an avatar'}])
    avatar.delete_avatar(curr_avatar.id, session)
    return user.delete_avatar_id(int(Authorize.get_jwt_subject()), session)


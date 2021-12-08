from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.app.dependencies import get_db
from src.models.user import UserLogin
from src.models.token import Token
from src.repositories import user

router = APIRouter(tags=["Auth"])
security = HTTPBearer()


@router.post("/login", status_code=200, response_model=Token)
async def login(user_info: UserLogin, session: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    curr_user = user.get_user_by_email(email=user_info.email, s=session)
    if not curr_user:
        raise HTTPException(status_code=400, detail='User with this email does not exist')
    if not user.validate_password(password=user_info.password, hashed_password=curr_user.hashed_password):
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    return user.create_user_token(id=curr_user.id, Authorize=Authorize)


@router.post("/token", status_code=200, response_model=Token)
async def refresh_token(Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_refresh_token_required()
    id = int(Authorize.get_jwt_subject())
    return user.create_user_token(id=id, Authorize=Authorize)
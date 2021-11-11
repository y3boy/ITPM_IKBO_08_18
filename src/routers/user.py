from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm

from src.schemas.user import UserBase
from src.schemas.walker import Walker
from src.schemas.dog import Dog
from src.database import crud
from src.app.dependencies import get_db
from src.schemas.user import TokenBase, UserLogin

router = APIRouter(prefix="/user", tags=["User"])
security = HTTPBearer()


@router.post("/auth", status_code=200)
async def auth_user(form_data: UserLogin, session: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = crud.user_read_by_username(username=form_data.login, session=session)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    if not crud.validate_password(password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    result = crud.create_user_token(user_id=user.id, session=session, Authorize=Authorize)
    return result


@router.post("/client", status_code=200)
async def create_client(user_info: UserBase, session: Session = Depends(get_db)):
    return crud.client_create(user_info, session)


@router.post("/walker", status_code=200)
async def create_walker(user_info: UserBase, walker_info: Walker, session: Session = Depends(get_db)):
    return crud.walker_create(user_arg=user_info, walker_arg=walker_info, session=session)


@router.patch("/", status_code=200)
async def update_user(user_info: UserBase, session: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return crud.user_update(int(Authorize.get_jwt_subject()), user_info, session)


@router.delete("/", status_code=200)
async def delete_user(session: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return crud.user_delete(int(Authorize.get_jwt_subject()), session)


@router.post("/dog", status_code=200)
async def create_dog(dog_info: Dog, session: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return crud.create_dog(user_id=int(Authorize.get_jwt_subject()), dog_arg=dog_info, session=session)


@router.get("/", status_code=200)
async def get_user(session: Session = Depends(get_db),
                   Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return crud.dog_read(int(Authorize.get_jwt_subject()), session)


@router.get("/walker", status_code=200)
async def get_walker(session: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return crud.walker_read(int(Authorize.get_jwt_subject()), session)


@router.get("/client", status_code=200)
async def get_client(session: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return crud.client_read(int(Authorize.get_jwt_subject()), session)


@router.get("/dog", status_code=200)
async def get_all_user_dog(session: Session = Depends(get_db),
                           Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return crud.get_all_user_dog(int(Authorize.get_jwt_subject()), session)
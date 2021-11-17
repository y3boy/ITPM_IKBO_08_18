from fastapi import APIRouter, Depends, Security
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.crud import walker as walker_crud
from src.app.dependencies import get_db
from src.schemas.user import UserBase
from src.schemas.walker import Walker, WalkerCreate, WalkerEdit

router = APIRouter(prefix="/walker", tags=["Walker"])
security = HTTPBearer()


@router.post("/", status_code=200)
async def create_walker(user_info: UserBase, walker_info: WalkerCreate, session: Session = Depends(get_db)):
    return walker_crud.create_walker(user_arg=user_info, walker_arg=walker_info, session=session)


@router.get("/", status_code=200)
async def get_walker(session: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return walker_crud.get_walker(int(Authorize.get_jwt_subject()), session)


@router.get("/all", status_code=200)
async def get_all_walker(session: Session = Depends(get_db)):
    return walker_crud.get_all_walker(session)


@router.patch("/", status_code=200)
async def set_walker(walker_info: WalkerEdit, session: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return walker_crud.set_walker(int(Authorize.get_jwt_subject()), walker_info, session)
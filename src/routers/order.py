from fastapi import APIRouter, Depends, Security
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.crud import order as order_crud
from src.app.dependencies import get_db
from src.schemas.order import OrderBase, OrderEdit

router = APIRouter(prefix="/order", tags=["Order"])
security = HTTPBearer()


@router.post("/", status_code=200)
async def create_order_for_client(order_info: OrderBase, session: Session = Depends(get_db),
                                  Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return order_crud.create_order_for_client(user_id=int(Authorize.get_jwt_subject()), order_arg=order_info, session=session)


@router.get("/client", status_code=200)
async def get_all_user_order_for_client(session: Session = Depends(get_db),
                           Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return order_crud.get_all_user_order_for_client(int(Authorize.get_jwt_subject()), session)


@router.get("/walker", status_code=200)
async def get_all_user_order_for_walker(session: Session = Depends(get_db),
                           Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return order_crud.get_all_user_order_for_walker(int(Authorize.get_jwt_subject()), session)


@router.patch("/", status_code=200)
async def set_order(order_id: int, order_info: OrderEdit, session: Session = Depends(get_db)):
    return order_crud.set_order(order_id, order_info, session)


@router.delete("/", status_code=200)
async def delete_order(order_id: int, session: Session = Depends(get_db)):
    return order_crud.delete_order(order_id, session)
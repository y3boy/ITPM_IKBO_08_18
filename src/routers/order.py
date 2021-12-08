from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.app.dependencies import get_db
from src.models.order import OrderOut, OrderUpdate, OrderCreate
from src.models.general import OrderUserDog
from src.repositories import order

router = APIRouter(prefix="/order", tags=["Order"])
security = HTTPBearer()


@router.get("/", status_code=200, response_model=OrderOut)
async def get_order_by_id(id: int, session: Session = Depends(get_db)):
    return order.get_order_by_id(id=id, s=session)


@router.get("/client_all", status_code=200, response_model=List[OrderUserDog])
async def get_all_current_client_order(session: Session = Depends(get_db),
                                       Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    mappers = order.get_all_client_order(int(Authorize.get_jwt_subject()), s=session)
    return [OrderUserDog(Order=i.Order, User=i.User, Dog=i.Dog) for i in mappers]


@router.get("/walker_all", status_code=200, response_model=List[OrderOut])
async def get_all_current_walker_order(session: Session = Depends(get_db),
                                       Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    mappers = order.get_all_walker_order(int(Authorize.get_jwt_subject()), s=session)
    return [OrderUserDog(Order=i.Order, User=i.User, Dog=i.Dog) for i in mappers]


@router.post("/", status_code=200, response_model=OrderOut)
async def create_order(order_info: OrderCreate, walker_user_id: int, dog_id: int, session: Session = Depends(get_db),
                       Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return order.create_order(o=order_info,
                              client_user_id=int(Authorize.get_jwt_subject()),
                              walker_user_id=walker_user_id,
                              dog_id=dog_id,
                              s=session)


@router.patch("/", status_code=200, response_model=OrderOut)
async def update_order(order_info: OrderUpdate, order_id: int, session: Session = Depends(get_db),
                       Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    curr_order = order.edit_order(o=order_info, id=order_id, user_id=int(Authorize.get_jwt_subject()), s=session)
    if not curr_order:
        raise HTTPException(status_code=400, detail='Access error')
    return curr_order

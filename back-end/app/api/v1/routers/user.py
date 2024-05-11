from typing import Annotated, List

from fastapi import APIRouter, Depends

from schemas.user import UserInDB, User, UserUpdate
from services.user import get_user_by_username, get_all_users, create_user, update_user, delete_by_username
from core.security import get_current_active_user, get_current_active_admin


user_router = APIRouter(prefix='/v1')


@user_router.get('/users/me/', response_model=User, tags=['user'], status_code=200)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@user_router.get('/users/{username}', response_model=UserInDB, tags=['user'], status_code=200)
def get_user(username: str, current_user: User = Depends(get_current_active_admin)) -> UserInDB:
    return get_user_by_username(username)


@user_router.get('/users', response_model=List[UserInDB], tags=['user'], status_code=200)
def get_users(current_user: User = Depends(get_current_active_admin)) -> List[UserInDB]:
    return get_all_users()


@user_router.post('/users', response_model=UserInDB, tags=['user'], status_code=201)
def post_user(user_data: UserInDB) -> UserInDB:
    return create_user(user_data)


@user_router.put('/users/{username}', response_model=UserInDB, tags=['user'], status_code=200)
def put_user(username: str, user_data: UserUpdate, current_user: User = Depends(get_current_active_admin)) -> UserInDB:
    return update_user(username, user_data)


@user_router.delete('/users/{username}', response_model=bool, tags=['user'], status_code=200)
def delete_user(username: str, current_user: User = Depends(get_current_active_admin)) -> bool:
    return delete_by_username(username)

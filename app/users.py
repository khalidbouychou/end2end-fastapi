import uuid 
from typing import Optional
from fastapi import Depends,Request
from fastapi_users import BaseUserManager , FastAPIUsers , UUIDIDMixin , models
from fastapi_users.authentication import AuthenticationBackend , BearerTransport , JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from app.db import User , get_async_session , get_user_db 



SECRET = "G712178_1337"


class UserManager(BaseUserManager[User , uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET


    async def  on_after_register(self , user : User , request : Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self , user : User , request : Optional[Request] = None):
        print(f"User {user.id} has forgot password.")

    # async def on_after_reset_password(self , user : User , request : Optional[Request] = None):
    #     print(f"User {user.id} has reset password.")

    async def on_after_request_verify(self , user : User , request : Optional[Request] = None):
        print(f"User {user.id} has requested to verify.")

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

# authentication backend 
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login") #means that the token url is auth/jwt/login


def get_jwt_strategy():
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

#means that the authentication backend is jwt and it uses bearer transport and jwt strategy
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

#means that the fastapi_users is a FastAPIUsers instance
fastapi_users= FastAPIUsers[User , uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True) #means that the current user is active

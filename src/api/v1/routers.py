from .auth import auth_router
from .user import user_router

all_routers = [auth_router, user_router]

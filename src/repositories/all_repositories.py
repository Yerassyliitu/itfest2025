from .base import SQLAlchemyRepository
from src.models.user import UserDTO


class UserRepository(SQLAlchemyRepository):
    model = UserDTO
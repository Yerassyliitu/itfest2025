from src.repositories.all_repositories import UserRepository
from src.services.user import UserService
from src.services.auth_service import AuthService


def get_user_service():
    user_repository = UserRepository()
    return UserService(user_repository)


def get_auth_service():
    return AuthService()
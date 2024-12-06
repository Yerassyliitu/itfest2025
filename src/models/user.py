from sqlalchemy import Column, String, BigInteger
from src.schemas.user import UserRead
from settings.database import Base


class UserDTO(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    email = Column(String, unique=True, nullable=True)
    
    def to_read_model(self) -> UserRead:
        return UserRead(
            id=self.id,
            email=self.email,
        )

    def get_hashed_password(self) -> str:
        return str(self.hashed_password)
from uuid import UUID

from sqlalchemy.orm import Session
from app.constants.user_role import UserRole
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, request: UserCreate) -> User:

        user = User(
            email=request.email,
            username=request.username,
            full_name=request.full_name,
            password=request.password,
            status=int(request.status),
            role=int(request.role),
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def update(self, user: User) -> User:

        self.db.commit()
        self.db.refresh(user)

        return user

    def find_all(self):

        return self.db.query(User).filter(User.role != UserRole.SUPERADMIN).all()

    def find_by_id(self, user_id: UUID):

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def find_by_email(self, email: str):

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def find_by_username(self, username: str):

        return (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )

    def delete(self, user: User):

        self.db.delete(user)
        self.db.commit()
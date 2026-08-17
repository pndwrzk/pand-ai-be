from app.constants.user_role import UserRole
from app.constants.user_status import UserStatus
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate

SUPERADMIN_EMAIL = "superadmin@pand.ai"
SUPERADMIN_USERNAME = "superadmin"
SUPERADMIN_FULL_NAME = "Super Admin"
SUPERADMIN_PASSWORD = "secret"


def run() -> None:

    db = SessionLocal()
    repository = UserRepository(db)

    try:
        existing = repository.find_by_email(SUPERADMIN_EMAIL)

        if existing:
            existing.role = int(UserRole.SUPERADMIN)
            existing.status = int(UserStatus.ACTIVE)
            existing.password = hash_password(SUPERADMIN_PASSWORD)
            existing.full_name = SUPERADMIN_FULL_NAME

            repository.update(existing)

            print(f"Superadmin updated successfully: {existing.email} (id={existing.id})")
            print(f"Login with email: {SUPERADMIN_EMAIL} / password: {SUPERADMIN_PASSWORD}")
            return

        user = UserCreate(
            email=SUPERADMIN_EMAIL,
            username=SUPERADMIN_USERNAME,
            full_name=SUPERADMIN_FULL_NAME,
            password=hash_password(SUPERADMIN_PASSWORD),
            status=UserStatus.ACTIVE,
            role=UserRole.SUPERADMIN,
        )

        created = repository.create(user)

        print(f"Superadmin created successfully: {created.email} (id={created.id})")
        print(f"Login with email: {SUPERADMIN_EMAIL} / password: {SUPERADMIN_PASSWORD}")

    finally:
        db.close()


if __name__ == "__main__":
    run()
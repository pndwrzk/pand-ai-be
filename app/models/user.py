from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
    )

    password: Mapped[str] = mapped_column(
        String(255),
    )
    
    status: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    role: Mapped[int] = mapped_column(
            Integer,
            default=0,
            nullable=False,
    )
     
    created_by: Mapped[UUID | None] = mapped_column(
            PGUUID(as_uuid=True),
            ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
            index=True,
        )
    
    updated_by: Mapped[UUID | None] = mapped_column(
            PGUUID(as_uuid=True),
            ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
            index=True,
        )
    
    created_at: Mapped[datetime] = mapped_column(
            DateTime,
            default=datetime.utcnow,
        )
    
    updated_at: Mapped[datetime] = mapped_column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        )
    
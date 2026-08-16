from contextvars import ContextVar
from typing import TypeVar
from uuid import UUID

from sqlalchemy import event
from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    pass


class AuditMixin:
    created_by: Mapped[UUID | None]
    updated_by: Mapped[UUID | None]


T = TypeVar("T", bound=AuditMixin)

_current_user_id: ContextVar[UUID | str | None] = ContextVar("_current_user_id", default=None)


def set_current_user_id(user_id: UUID | str | None) -> None:
    _current_user_id.set(user_id)


def clear_current_user_id() -> None:
    _current_user_id.set(None)


def _apply_audit_fields(instance: T, user_id: UUID | str | None, *, is_create: bool) -> None:
    if user_id is None:
        return

    # Convert string user_id to UUID
    audit_user_id = UUID(user_id) if isinstance(user_id, str) else user_id

    if hasattr(instance, "created_by") and is_create and getattr(instance, "created_by", None) is None:
        instance.created_by = audit_user_id

    if hasattr(instance, "updated_by"):
        instance.updated_by = audit_user_id


@event.listens_for(Base, "before_insert", propagate=True)
def _before_insert(mapper, connection, target):
    user_id = _current_user_id.get()
    _apply_audit_fields(target, user_id, is_create=True)


@event.listens_for(Base, "before_update", propagate=True)
def _before_update(mapper, connection, target):
    user_id = _current_user_id.get()
    _apply_audit_fields(target, user_id, is_create=False)

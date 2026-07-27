from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_proj.database.mixins.id_mixins import IDMixin
from fastapi_proj.database.mixins.timestamp_mixins import TimestampsMixin
from fastapi_proj.database.models.base import Base


class User(IDMixin, TimestampsMixin, Base):
    """
    Класс User представляет пользователя в системе.

    :ivar email: Email адрес пользователя.
    :type email: str
    :ivar hashed_password: Хэшированный пароль пользователя.
    :type hashed_password: str
    :ivar is_active: Флаг активности пользователя (True или False).
    :type is_active: bool
    :ivar is_superuser: Флаг суперпользователя (True или False).
    :type is_superuser: bool
    :ivar is_verified: Флаг подтверждения аккаунта (True или False).
    :type is_verified: bool
    """

    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

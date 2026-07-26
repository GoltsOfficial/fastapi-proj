from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from fastapi_proj.core.settings import settings  # ← поправь под своё имя пакета


class DBDependency:
    def __init__(self) -> None:
        self._engine = create_async_engine(
            url=settings.db_settings.db_url,
            echo=settings.db_settings.db_echo,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autocommit=False,
        )

    @property
    def db_session(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

    @property
    def db_engine(self) -> AsyncEngine:
        return self._engine

from fastapi import Depends, HTTPException
from itsdangerous import BadSignature, URLSafeTimedSerializer
from starlette import status
from starlette.responses import JSONResponse

from fastapi_proj.apps.auth.handlers import AuthHandler
from fastapi_proj.apps.auth.managers import UserManager
from fastapi_proj.apps.auth.schemas import (
    AuthUser,
    CreateUser,
    UserReturnData,
    UserVerifySchema,
)
from fastapi_proj.apps.auth.tasks import send_confirmation_email
from fastapi_proj.core.settings import settings


class UserService:
    """
    Класс для управления пользователями.
    """

    def __init__(
        self,
        manager: UserManager = Depends(UserManager),
        handler: AuthHandler = Depends(AuthHandler),
    ) -> None:
        """
        Инициализирует экземпляр класса, используя зависимости для управления пользователями и авторизации.

        :param manager: Управитель пользователей, отвечающий за CRUD-операции над пользователями.
        :type manager: UserManager
        :param handler: Обработчик аутентификации и авторизации, который используется для проверки доступа к ресурсам.
        :type handler: AuthHandler
        """
        self.manager = manager
        self.handler = handler
        self.serializer = URLSafeTimedSerializer(secret_key=settings.secret_key.get_secret_value())

    async def register_user(self, user: AuthUser) -> UserReturnData:
        """
        Регистрирует нового пользователя в системе.

        :param user: Информация о пользователе, который нужно зарегистрировать.
        :type user: AuthUser
        :returns: Данные о созданном пользователе.
        :rtype: UserReturnData
        """
        hashed_password = await self.handler.get_password_hash(user.password)

        new_user = CreateUser(email=user.email, hashed_password=hashed_password)

        user_data = await self.manager.create_user(user=new_user)

        confirmation_token = self.serializer.dumps(user_data.email)
        send_confirmation_email.delay(to_email=user_data.email, token=confirmation_token)

        return user_data

    async def confirm_user(self, token: str) -> None:
        """
        Подтверждает пользователя по переданному токену.

        :param token: Токен для подтверждения пользователя.
        :type token: str
        :raises HTTPException: Если токен неверный или просроченный.
        """
        try:
            email = self.serializer.loads(token, max_age=3600)
        except BadSignature:
            raise HTTPException(status_code=400, detail="Неверный или просроченный токен")

        await self.manager.confirm_user(email=email)

    async def login_user(self, user: AuthUser) -> JSONResponse:
        """
        Вход пользователя в систему.

        :param user: Объект пользователя с входными данными для аутентификации.
        :type user: AuthUser
        :returns: Ответ сервера, указывающий на успешность или неудачу входа.
        :rtype: JSONResponse
        :raises HTTPException: Если предоставленные учетные данные неверны (HTTP 401 Unauthorized).
        """
        exist_user = await self.manager.get_user_by_email(email=user.email)

        if exist_user is None or not await self.handler.verify_password(
            hashed_password=exist_user.hashed_password, raw_password=user.password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong email or password",
            )

        token, session_id = await self.handler.create_access_token(user_id=exist_user.id)

        await self.manager.store_access_token(token=token, user_id=exist_user.id, session_id=session_id)

        response = JSONResponse(content={"message": "Вход успешен"})
        response.set_cookie(
            key="Authorization",
            value=token,
            httponly=True,
            max_age=settings.access_token_expire,
        )

        return response

    async def logout_user(self, user: UserVerifySchema) -> JSONResponse:
        """
        Отправляет запрос на выход пользователя из системы.

        :param user: Схема, содержащая информацию о пользователе для аутентификации.
        :type user: UserVerifySchema
        :returns: Ответ сервера с сообщением об успешном выходе пользователя.
        :rtype: JSONResponse
        :raises Exception: Если произошла ошибка при отмене токена доступа.
        """
        await self.manager.revoke_access_token(user_id=user.id, session_id=user.session_id)

        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie(key="Authorization")

        return response

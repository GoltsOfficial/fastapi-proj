from typing import NamedTuple


class CreateTokenTuple(NamedTuple):
    """
    Класс для создания кортежа токенов, содержащего закодированный JWT и идентификатор сессии.

    Класс наследует от `NamedTuple` и представляет собой неизменяемый контейнер для хранения двух значений:
        - закодированного JSON Web Token (JWT)
        - уникального идентификатора сессии.

    :ivar encoded_jwt: Закодированный JWT-токен.
    :type encoded_jwt: str
    :ivar session_id: Уникальный идентификатор сессии.
    :type session_id: str
    """

    encoded_jwt: str
    session_id: str

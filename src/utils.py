import asyncio
from typing import Callable
from functools import wraps

from src.exceptions import RetryException
from src.logging_config import LOGGER


def retry(num: int, delay: float):
    """
    Декоратор для повторного запуска функции в случае неудачного выполнения.

    num - количество раз перезапуска функции
    delay - задержка в секундах перед повторами
    """
    def decorator(func: Callable):
        @wraps(func)
        async def inner(*args, **kwargs):
            for i in range(num):
                try:
                    result = await func(*args, **kwargs)
                    if result:
                        return result
                    LOGGER.exception(f"Неудачная попытка выполнения функции {func.__name__}. "
                                     f"Выполняем {i+1}ый раз")
                except Exception as e:
                    LOGGER.exception(f"При выполнении функции {func.__name__} получено исключение: {e}. "
                                     f"Выполняем {i+1}ый раз")
                await asyncio.sleep(delay)
            raise RetryException(f"Функция {func.__name__} не смогла успешно отработать")
        return inner
    return decorator

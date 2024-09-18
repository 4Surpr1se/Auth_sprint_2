import datetime
from fastapi import Request, HTTPException
from db.redis import redis_client  # Импортируем асинхронный Redis клиент

# Лимиты запросов
REQUEST_LIMIT_PER_MINUTE = 20


async def rate_limiter(request: Request):
    user_id = request.client.host  # Используем IP адрес пользователя
    now = datetime.datetime.now()

    # Генерируем ключ на основе IP и текущей минуты
    key = f"{user_id}:{now.minute}"

    # Используем redis-client для асинхронных операций
    async with redis_client.pipeline(transaction=True) as pipe:
        # Увеличиваем количество запросов и задаем время жизни ключа
        pipe.incr(key, 1)
        pipe.expire(key, 59)
        result = await pipe.execute()

    # Получаем текущее количество запросов
    request_number = result[0]

    # Если количество запросов превышает лимит
    if request_number > REQUEST_LIMIT_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Too many requests. Try again later.")

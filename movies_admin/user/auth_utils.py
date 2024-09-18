import uuid
from typing import List, Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from pydantic import BaseModel, field_validator

User = get_user_model()


class UserModel(BaseModel):
    id: uuid.UUID
    roles: List[Any]
    username: str
    email: str
    is_active: bool


# todo Также подключить, чтобы сначала запрос шел на пермишены и роли и сравнивалось по айди а не имени
def _get_user_from_dict(data):
    if "ADMIN" in [k['name'] for k in data['roles']]:
        return User.objects.create_superuser(**UserModel(**data).model_dump())
    return AnonymousUser()

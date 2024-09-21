from typing import Callable, Annotated
from services.user_service import UserService, get_user_service
from services.auth_service import AuthJWTService, get_auth_service

import httpx
from fastapi import Query, HTTPException, status

from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from services.oauth_service import oauth
from db.database import get_db

from core.config import settings

router = APIRouter()


class OauthParams:

    def __init__(
            self,
            access_token: str = Query(
                1,
                title="Provider access_token.",

            ),
            cid: str = Query(
                50,
                title="Provider cid."
            ),
    ):
        self.access_token = access_token
        self.cid = cid


@router.get("/login/{provider}")
async def login(provider: str, request: Request):
    if provider_urls := settings.providers_mapper.get(provider):
        client_id = settings.yandex_client_id
        auth_url = f"{provider_urls['login']}{client_id}"
        return {"auth_url": auth_url}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Provider {provider} does not supported",
    )

@router.get("/auth/callback/{provider}")
async def auth_callback(params: Annotated[OauthParams, Depends()], provider: str,
                        user_service: UserService = Depends(get_user_service),
                        auth_service: AuthJWTService = Depends(get_auth_service)):
    if provider_urls := settings.providers_mapper.get(provider):
        headers = {"Authorization": f"OAuth {params.access_token}"}
        response = await httpx.AsyncClient().get(
            provider_urls["callback"], headers=headers
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info",
            )
        user_info = response.json()

    # Проверка существующего пользователя или создание нового
    user = user_service.get_or_create_user_oauth(provider, user_info)
    auth_data = await auth_service.login(user)
    # Логика авторизации (например, установка сессии)
    return auth_data

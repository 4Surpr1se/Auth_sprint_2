import typer
from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import ORJSONResponse

from api.v1 import auth, role, permission, user, oauth
from commands import cli_app
from core.config import settings
from core.lifespan import lifespan
from decorators.permissions import get_current_user_global
from core.tracing import init_tracer

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)
# Middleware для добавления ограничения количества запросов

# @app.middleware("http")
# async def add_rate_limiting(request: Request, call_next):
#     await rate_limiter(request)  # Применяем ограничение запросов
#     response = await call_next(request)
#     return response


# Инициализация трассировки
init_tracer(app)

# Middleware для трассировки и добавления  x-request-id
@app.middleware("http")
async def add_request_id_header(request: Request, call_next):
    # Получаем x-request-id из заголовков или создаем новый
    request_id = request.headers.get("x-request-id", None)
    if not request_id:
        request_id = "generated-request-id"  # Можно использовать uuid4 для генерации

    # Логируем запрос с x-request-id
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"], dependencies=[Depends(get_current_user_global)])
app.include_router(role.router, prefix="/api/v1/roles", tags=["roles"], dependencies=[Depends(get_current_user_global)])
app.include_router(
    permission.router,
    prefix="/api/v1/permissions",
    tags=["permissions"],
    dependencies=[
        Depends(get_current_user_global)])
app.include_router(user.router, prefix="/api/v1/users", tags=["users"], dependencies=[Depends(get_current_user_global)])

app.include_router(oauth.router, prefix="/api/v1/oauth", tags=["oauth"])

# Создаем новый Typer приложение для CLI команд
cli = typer.Typer()
cli.add_typer(cli_app, name="app")

if __name__ == "__main__":
    cli()

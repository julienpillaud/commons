from fastapi import FastAPI

from app.api.exception_handlers import ExceptionHandlers
from app.api.routes.posts import router as posts_router
from app.api.routes.users import router as users_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(posts_router)
    app.include_router(users_router)

    ExceptionHandlers(app)

    return app

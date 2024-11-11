from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import TooManyTagsError
from app.infrastructure.exceptions import (
    DatabaseError,
    EntityAlreadyExistsError,
    EntityNotFoundError,
)


class ExceptionHandlers:
    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.register_handlers()

    def register_handlers(self) -> None:
        self.app.exception_handler(EntityNotFoundError)(self.handle_entity_not_found)
        self.app.exception_handler(EntityAlreadyExistsError)(
            self.handle_entity_already_exists
        )
        self.app.exception_handler(DatabaseError)(self.handle_database_error)
        self.app.exception_handler(TooManyTagsError)(self.handle_too_many_tags)

    @staticmethod
    async def handle_entity_not_found(
        request: Request, exc: EntityNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": str(exc),
                "type": exc.entity_type,
                "id": exc.entity_id,
            },
        )

    @staticmethod
    async def handle_entity_already_exists(
        request: Request, exc: EntityAlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "message": str(exc),
                "type": exc.entity_type,
            },
        )

    @staticmethod
    async def handle_database_error(
        request: Request, exc: DatabaseError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL,
            content={
                "message": f"Database {exc.operation} failed",
                "detail": exc.details,
            },
        )

    @staticmethod
    async def handle_too_many_tags(
        request: Request, exc: TooManyTagsError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": str(exc),
                "max_tags": exc.max_tags,
            },
        )

from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.domain.exceptions import HTTPException


def create_app():
    app = FastAPI()

    @app.exception_handler(HTTPException)
    async def exception_handler(_, exception: HTTPException):
        return JSONResponse(
            status_code=exception.status_code,
            content={"error_body": {"title": exception.title, "message": exception.message}}
        )


    return app
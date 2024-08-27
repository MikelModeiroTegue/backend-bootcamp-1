import uvicorn

from app import create_app
from app.api import api
from app.data.database import create_tables

app = create_app()

create_tables()

app.include_router(api.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=9000)
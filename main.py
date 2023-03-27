import uvicorn
from fastapi import FastAPI

from source.api.auth.user_router import user_router
from source.api.routers.courses import courses_router
from source.api.routers.groups import groups_router
from source.api.routers.students import students_router


def init_app() -> FastAPI:
    fastapi = FastAPI()
    fastapi.include_router(students_router)
    fastapi.include_router(courses_router)
    fastapi.include_router(groups_router)
    fastapi.include_router(user_router)
    return fastapi


app = init_app()


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)

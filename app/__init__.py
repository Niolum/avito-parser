from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()

    from .views import router
    app.include_router(router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app
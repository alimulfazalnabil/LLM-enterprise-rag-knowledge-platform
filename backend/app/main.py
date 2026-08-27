from fastapi import FastAPI

from .api.v1.routes import router as v1_router
from .core.config import settings
from .database import get_db, init_db
from .services.documents import ensure_demo_resources


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.include_router(v1_router)

    @app.get("/health")
    def health():
        return {"status": "ok", "environment": settings.app_env}

    @app.get("/health/live")
    def live():
        return {"status": "alive"}

    @app.get("/health/ready")
    def ready():
        return {"status": "ready", "dependencies": {"database": "ok"}}

    return app


app = create_app()
init_db()
db = next(get_db())
try:
    ensure_demo_resources(db)
finally:
    db.close()

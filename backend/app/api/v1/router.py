from fastapi import APIRouter

from app.api.v1 import (
    admin,
    auth,
    chat,
    documents,
    evaluation,
    routes_health,
    routes_metrics,
    search,
)

api_router = APIRouter()
api_router.include_router(routes_health.router, tags=['health'])
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(documents.router, prefix='/documents', tags=['documents'])
api_router.include_router(search.router, tags=['search'])
api_router.include_router(chat.router, tags=['chat'])
api_router.include_router(evaluation.router, prefix='/evaluation', tags=['evaluation'])
api_router.include_router(admin.router, tags=['admin'])
api_router.include_router(routes_metrics.router, tags=['metrics'])

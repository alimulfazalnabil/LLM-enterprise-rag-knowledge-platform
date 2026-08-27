from fastapi import APIRouter

from app.api.v1 import routes_auth, routes_chat, routes_documents, routes_evaluation, routes_health, routes_metrics, routes_search

api_router = APIRouter()
api_router.include_router(routes_health.router, tags=['health'])
api_router.include_router(routes_auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(routes_documents.router, prefix='/documents', tags=['documents'])
api_router.include_router(routes_search.router, tags=['search'])
api_router.include_router(routes_chat.router, tags=['chat'])
api_router.include_router(routes_evaluation.router, prefix='/evaluation', tags=['evaluation'])
api_router.include_router(routes_metrics.router, tags=['metrics'])

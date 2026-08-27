from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SearchRequest(BaseModel):
    query: str

@router.post('/search')
def search(_: SearchRequest) -> dict:
    return {'results': [], 'mode': 'hybrid'}

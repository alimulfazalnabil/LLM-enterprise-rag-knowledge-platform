from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post('/chat')
def chat(_: ChatRequest) -> dict:
    return {
        'answer': "I don't have enough information in the available knowledge base to answer this reliably.",
        'grounded': False,
        'citations': [],
        'retrieval': {
            'dense_results': 0,
            'sparse_results': 0,
            'fusion_results': 0,
            'reranked_results': 0,
        },
        'metrics': {'latency_ms': 0},
    }

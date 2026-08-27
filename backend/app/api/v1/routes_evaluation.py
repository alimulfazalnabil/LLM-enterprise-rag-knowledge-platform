from fastapi import APIRouter

router = APIRouter()

@router.get('/runs')
def list_runs() -> dict[str, list]:
    return {'runs': []}

@router.post('/run')
def run_eval() -> dict[str, str]:
    return {'status': 'Benchmark pending execution.'}

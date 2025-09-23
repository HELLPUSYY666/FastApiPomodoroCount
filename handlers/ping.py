from fastapi import APIRouter
from settings import Settings

router = APIRouter(prefix='/ping', tags=['ping'])


@router.get('/db')
async def ping():
    settings = Settings()
    return {'message': settings.GOOGLE_TOKEN_ID}


@router.get('/app')
async def app():
    return {'message': 'app'}

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, chat, image, tts
from app.db import models
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="Fluukpe Backend")

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

app.include_router(auth.router, prefix='/api/auth', tags=['auth'])
app.include_router(chat.router, prefix='/api', tags=['chat'])
app.include_router(image.router, prefix='/api', tags=['image'])
app.include_router(tts.router, prefix='/api', tags=['tts'])

@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get('/')
async def root():
    return {'status':'ok'}

if __name__ == '__main__':
    uvicorn.run('app.main:app', host='0.0.0.0', port=8080, reload=True)

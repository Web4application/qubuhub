from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from app.api.deps import get_current_user
from app.db.session import AsyncSessionLocal
from app.db import models
from sqlalchemy import insert
import os, httpx

router = APIRouter()

class TTSIn(BaseModel):
    text: str

@router.post('/tts')
async def tts_endpoint(payload: TTSIn, user = Depends(get_current_user)):
    OPENAI_KEY = os.getenv('OPENAI_API_KEY')
    if OPENAI_KEY:
        headers = {'Authorization': f'Bearer {OPENAI_KEY}', 'Content-Type':'application/json'}
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream('POST','https://api.openai.com/v1/audio/speech', headers=headers, json={
                "model":"gpt-4o-mini-tts","voice":"alloy","input":payload.text
            }) as r:
                r.raise_for_status()
                audio_bytes = b''
                async for chunk in r.aiter_bytes():
                    audio_bytes += chunk
    else:
        audio_bytes = b''
    async with AsyncSessionLocal() as session:
        await session.execute(insert(models.TTSLog).values(user_id=user.id, text=payload.text, audio_url="stream"))
        await session.commit()
    return Response(content=audio_bytes, media_type='audio/mpeg')

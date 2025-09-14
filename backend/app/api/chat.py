from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.deps import get_current_user
from app.db.session import AsyncSessionLocal
from app.db import models
from sqlalchemy import insert
import httpx, os

router = APIRouter()

class ChatIn(BaseModel):
    prompt: str

@router.post('/chat')
async def chat_endpoint(payload: ChatIn, user = Depends(get_current_user)):
    OPENAI_KEY = os.getenv('OPENAI_API_KEY')
    headers = {'Authorization': f'Bearer {OPENAI_KEY}'} if OPENAI_KEY else {}
    async with httpx.AsyncClient() as client:
        if OPENAI_KEY:
            r = await client.post('https://api.openai.com/v1/chat/completions', headers=headers, json={
                "model":"gpt-5-mini",
                "messages":[{"role":"user","content":payload.prompt}],
                "max_tokens":512
            })
            data = r.json()
            reply = data.get('choices',[{}])[0].get('message',{}).get('content','')
        else:
            reply = f"(dev) Echo: {payload.prompt}"
    async with AsyncSessionLocal() as session:
        await session.execute(insert(models.ChatLog).values(user_id=user.id, prompt=payload.prompt, response=reply))
        await session.commit()
    return {"reply": reply}

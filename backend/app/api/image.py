from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.deps import get_current_user
from app.db.session import AsyncSessionLocal
from app.db import models
from sqlalchemy import insert
import os, httpx

router = APIRouter()

class ImageIn(BaseModel):
    prompt: str

@router.post('/image')
async def image_endpoint(payload: ImageIn, user = Depends(get_current_user)):
    REPLICATE_TOKEN = os.getenv('REPLICATE_API_KEY')
    if REPLICATE_TOKEN:
        async with httpx.AsyncClient() as client:
            r = await client.post('https://api.replicate.com/v1/predictions', headers={
                'Authorization': f'Token {REPLICATE_TOKEN}', 'Content-Type':'application/json'
            }, json={"version":"stability-ai/stable-diffusion","input":{"prompt":payload.prompt}})
            data = r.json()
            url = data.get('output',[None])[0] if isinstance(data.get('output'), list) else None
    else:
        url = f"https://dummyimage.com/1024x768/000/fff&text={payload.prompt.replace(' ','+')}"
    async with AsyncSessionLocal() as session:
        await session.execute(insert(models.ImageLog).values(user_id=user.id, prompt=payload.prompt, url=url))
        await session.commit()
    return {"url": url}

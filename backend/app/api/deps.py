from fastapi import Depends, HTTPException, status
from jose import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from sqlalchemy.future import select
from app.db import models
from app.db.session import AsyncSessionLocal

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get('sub'))
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    async with AsyncSessionLocal() as session:
        q = await session.execute(select(models.User).where(models.User.id == user_id))
        user = q.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
    return user

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.future import select
from app.db.session import AsyncSessionLocal
from app.db import models
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

async def get_user_by_email(session, email):
    q = await session.execute(select(models.User).where(models.User.email == email))
    return q.scalars().first()

@router.post('/register', response_model=Token)
async def register(payload: RegisterIn):
    async with AsyncSessionLocal() as session:
        user = await get_user_by_email(session, payload.email)
        if user:
            raise HTTPException(status_code=400, detail='Email already registered')
        hashed = pwd_context.hash(payload.password)
        new = models.User(email=payload.email, hashed_password=hashed)
        session.add(new)
        await session.commit()
        await session.refresh(new)
        access_token = create_access_token({"sub": str(new.id)})
        return {"access_token": access_token, "token_type": "bearer"}

@router.post('/login', response_model=Token)
async def login(payload: RegisterIn):
    async with AsyncSessionLocal() as session:
        user = await get_user_by_email(session, payload.email)
        if not user or not pwd_context.verify(payload.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Invalid credentials')
        access_token = create_access_token({"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded

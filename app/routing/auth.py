from fastapi import APIRouter, Depends
from typing import Annotated
from app.database.schema.user_schema import UserSchema
from app.models.auth import Register, Login, RegisterResponse
from sqlalchemy.orm import Session
from app.database.db import get_db
from fastapi.responses import JSONResponse
from app.helper import hashPassword, verifyPassword, createAccessToken

router = APIRouter(prefix="/auth")


@router.post("/login")
def login(data: Login, db: Annotated[Session, Depends(get_db)]):
    user = db.query(UserSchema).filter(UserSchema.email == data.email).first()
    if not user or not verifyPassword(data.password, user.hashed_password):
        return JSONResponse({"message": "Invalid email or password"}, status_code=401)

    payload = {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
    token = createAccessToken(payload)
    payload["access_token"] = "Bearer " + token
    return {"message": "User logged in successfully", "data": payload}


@router.post("/register", response_model=RegisterResponse)
def register(data: Register, db: Annotated[Session, Depends(get_db)]):
    # Check if user already exists
    existing_user = db.query(UserSchema).filter(UserSchema.email == data.email).first()
    if existing_user:
        return JSONResponse({"message": "User already exists"}, status_code=400)

    new_user = UserSchema(
        name=data.name,
        username=data.username,
        email=data.email,
        hashed_password=hashPassword(data.password),
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user": new_user}
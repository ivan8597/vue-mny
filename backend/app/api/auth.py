from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from jose import jwt
from datetime import datetime, timedelta
from app.api.deps import SECRET_KEY, ALGORITHM
from fastapi.responses import JSONResponse
from pydantic import ValidationError

router = APIRouter()

# Используем более специфичную конфигурацию
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Явно указываем количество раундов
)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    print(f"Registration attempt with data: {user_data.model_dump(exclude={'password'})}")
    
    try:
        # Проверяем существующего пользователя
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
            
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=400,
                detail="Username already taken"
            )

        # Создаем пользователя
        hashed_password = pwd_context.hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            name=user_data.name,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User created successfully"}
    except HTTPException as e:
        db.rollback()
        raise  # Пробрасываем HTTPException как есть
    except Exception as e:
        print(f"Registration error: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    print(f"Login attempt with: {form_data.username}")
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"} 
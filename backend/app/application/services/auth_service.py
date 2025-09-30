from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.domain.models.entities import User
from app.application.schemas.auth import UserCreate, UserLogin, Token
from app.main import db
import os

class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def create_access_token(self, data: dict) -> Token:
        to_encode = data.copy()
        expires_at = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expires_at})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return Token(access_token=encoded_jwt, expires_at=expires_at)

    async def register_user(self, user: UserCreate) -> Token:
        # Check if user exists
        if await db.users.find_one({"username": user.username}):
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Create new user
        hashed_password = self.get_password_hash(user.password)
        user_data = User(
            username=user.username,
            hashed_password=hashed_password,
            id=str(await db.users.count_documents({}))
        )
        
        await db.users.insert_one(user_data.dict())
        
        # Create access token
        return await self.create_access_token({"sub": user.username})

    async def login_user(self, user: UserLogin) -> Token:
        # Find user
        db_user = await db.users.find_one({"username": user.username})
        if not db_user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        # Verify password
        if not self.verify_password(user.password, db_user["hashed_password"]):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        # Create access token
        return await self.create_access_token({"sub": user.username})

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
            
        user = await db.users.find_one({"username": username})
        if user is None:
            raise credentials_exception
            
        return User(**user)

    async def refresh_token(self, current_token: str) -> Token:
        try:
            payload = jwt.decode(current_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return await self.create_access_token({"sub": username})
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
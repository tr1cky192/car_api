from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
import datetime
from passlib.context import CryptContext

app = FastAPI()

# Налаштування для OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Для хешування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Секретний ключ для JWT
SECRET_KEY = "reggsad"
ALGORITHM = "HS256"

# Модель для входу користувача
class User(BaseModel):
    username: str
    password: str

# Створення токену
def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    if expires_delta is None:
        expires_delta = datetime.timedelta(minutes=30)
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функція для отримання користувача по токену
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username


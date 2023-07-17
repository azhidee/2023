from jose import JWTError, jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import secrets
import string

length = 64
characters = string.ascii_lowercase + string.digits
# secret_key = ''.join(secrets.choice(characters) for i in range(length))
SECRET_KEY = "od7d3uwpzzgpklgcxvw70kmamdmbk02srfros9f5jjf3kf7lwxj1taax2ricdfq8"
ALGORITHM = "HS256"


class TokenData(BaseModel):
    username: str = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth_schema = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algoritm=ALGORITHM)

    return encoded_jwt


class UserInDB(BaseModel):
    username: str
    hashed_password: str


def get_user(db, username:str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
    
def authenticate_user(fake_db, username:str, password:str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user



from jose import JWTError, jwt
from fastapi import FastAPI, Depends, HTTPException, status
from elasticsearch import Elasticsearch
from fastapi.security import OAuth2PasswordRequestForm
from authentication import (
    authenticate_user,
    create_access_token,
    oauth_schema,
    SECRET_KEY,
    ALGORITHM,
    TokenData,
    get_user,
)
from datetime import timedelta

app = FastAPI()

# es = Elasticsearch()
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

@app.get("/")
def read_root():
    return {"testK": "testV"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


ACCESS_TOKEN_EXPIRE_MINUTES = 30


def fake_hash_password(password: str):
    return "fakehashed" + password


users_db = {
    "john": {"username": "john", "hashed_password": fake_hash_password("secret")}
}


@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Athenticate": "Beare"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/")
async def read_users_me(token: str = Depends(oauth_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, token_data.username)
    if user is None:
        raise credentials_exception
    return user

from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv
from security import verify_password
from pathlib import Path
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import json

security = HTTPBearer()
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data: dict):
	to_encode = data.copy()
	
	expire = (
		datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
	)

	to_encode.update({"exp": expire})

	return jwt.encode(
		to_encode,
		SECRET_KEY,
		algorithm = ALGORITHM
	)
	
def authenticate_user(
	username: str,
	password: str
):
	USERS_FILE = Path(__file__).parent.parent / "user.json"

	with open(USERS_FILE, "r") as f:
		users = json.load(f)

	user = users.get(username)

	if not user:
		return None

	if not verify_password(
		password,
		user["password"]
	):
		return None

	return username

def verify_token(token: str):

	try:
		payload = jwt.decode(
			token,
			SECRET_KEY,
			algorithms=[ALGORITHM]
		)

		username = payload.get("sub")

		if username is None:
			return None

		return username

	except JWTError:
		return None

def get_current_user(
	credentials: HTTPAuthorizationCredentials = Depends(security)
):

	token = credentials.credentials

	username = verify_token(token)

	if username is None:
		raise HTTPException(
			status_code=401,
			detail="Invalid token"
		)

	return username


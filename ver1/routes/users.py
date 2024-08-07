import requests
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.users import User, TokenResponse

user_router = APIRouter(
    tags=["User"],
)

user_database = Database(User)
hash_password = HashPassword()

KAKAO_USERINFO_URL = "https://kapi.kakao.com/v2/user/me"


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    new_user = User(
            id=user.username,
            password=user.password
    )
    user_exist = await User.find_one(User.id == new_user.id)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User exists already."
        )
    hashed_password = hash_password.create_hash(new_user.password)
    new_user.password = hashed_password
    await user_database.save(new_user)
    return {
        "message": "User created successfully"
    }

@user_router.patch("/signin", response_model=TokenResponse)
async def signin(fcm: str, user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.id == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist."
        )
    if hash_password.verify_hash(user.password, user_exist.password):
        await User.update_one(
            {"id": user.id},
            {"$set": {"fcm_token": user.fcm_token}}
        )
        access_token = create_access_token(user_exist.id)
        return {
            "message": "User signined successfully",
            "access_token": access_token,
            "token_type": "Bearer"
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )

@user_router.post("/kakao", response_model=TokenResponse)
async def kakao_login(access_token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(KAKAO_USERINFO_URL, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Kakao access token."
        )

    user_info = response.json()
    phone_number = user_info.get("kakao_account", {}).get("phone_number")

    if not phone_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number not available in Kakao account."
        )

    user_exist = await User.find_one(User.id == phone_number)
    if not user_exist:
        new_user = User(
            id=phone_number[3:],
            password=hash_password.create_hash(phone_number[3:])  # 임시 비밀번호
        )
        await user_database.save(new_user)
        user_exist = new_user

    access_token = create_access_token(user_exist.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
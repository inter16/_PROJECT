import requests
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from models.users import User, TokenResponse, UpdateUser, SigninUser, SigninKakao
from typing import Optional

from auth.authenticate import authenticate

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
            password=user.password,
            sensors=[]
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


    
@user_router.patch("/signin")
async def signin(user:OAuth2PasswordRequestForm = Depends(),fcm:Optional[str]=None) -> dict:
    user_exist = await User.find_one(User.id == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist."
        )
    if hash_password.verify_hash(user.password, user_exist.password):
        if fcm:
            await user_exist.update({"$set": {"fcm": fcm}})
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


@user_router.patch("/kakao")
async def kakao_login(req:SigninKakao) -> dict:
    headers = {
        "Authorization": f"Bearer {req.token}"
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
            password=hash_password.create_hash(hash_password.create_hash(phone_number[3:])[:10]),
            fcm=req.fcm,
            sensors=[]
        )
        await user_database.save(new_user)
        user_exist = await User.find_one(User.id == phone_number)
    else:
        await user_exist.update({"$set": {"fcm": req.fcm}})
    access_token = create_access_token(user_exist.id)
    return {
        "message": "KaKao user signined successfully",
        "access_token": access_token,
        "token_type": "Bearer"
    }


@user_router.get("/getname")
async def get_name(id: str = Depends(authenticate)) -> dict:
    user_exist=await User.find_one(User.id == id)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist."
        )
    return {
        "Message" : f"Your name is {user_exist.name}"
    }

@user_router.patch("/edit")
async def user_name(req:UpdateUser, id: str = Depends(authenticate)) -> dict:
    user_exist=await User.find_one(User.id == id)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist."
        )
    await user_database.update(id,req)
    return {
        "Message" : "Update name successfully"
    }
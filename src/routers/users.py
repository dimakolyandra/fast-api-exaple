from fastapi import APIRouter

from fastapi import HTTPException
from sql_app import schemas, crud


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=schemas.UserBase)
async def create_user(user: schemas.UserCreate):
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user=user)


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int):
    db_user = await crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user1_id}/subscribe/{user2_id}")
async def subscribe_user(user1_id: int, user2_id: int):
    user1 = await crud.get_user(user_id=user1_id)
    if user1 is None:
        raise HTTPException(status_code=404, detail="User1 not found")
    user2 = await crud.get_user(user_id=user2_id)
    if user2 is None:
        raise HTTPException(status_code=404, detail="User2 not found")
    await crud.subscribe_user(user1, user2)
    return {"user_from_id": user1_id, "user_to_id": user2_id}


@router.get('/{user_id}/posts', response_model=schemas.UserPosts)
async def get_subscriptions(user_id: int):
    return await crud.get_user_subscription(user_id)


@router.post('/{user_id}/item', response_model=schemas.ItemCreateResponse)
async def create_item(user_id: int, item: schemas.ItemCreate):
    return await crud.create_user_item(item, user_id)

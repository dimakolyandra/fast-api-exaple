from sqlalchemy.future import select
from . import models, schemas


async def get_user(user_id: int):
    async with models.SessionLocal() as db_:
        stmt = select(models.User).filter(models.User.id == user_id)
        return (await db_.execute(stmt)).scalars().first()


async def get_user_subscription(user_id: int):
    async with models.SessionLocal() as db_:
        items_db = select(models.Item)\
            .join(models.UserSubs, models.UserSubs.subscribe_to_id == models.Item.owner_id)\
            .join(models.User, models.UserSubs.subscriber_id == models.User.id)\
            .where(models.UserSubs.subscriber_id == user_id)\
            .limit(10)\
            .order_by(models.Item.id.desc())
        items_db = (await db_.execute(items_db)).unique().scalars()
    return schemas.UserPosts(
        id=user_id,
        posts=list(items_db),
    )


async def get_user_by_email(email: str):
    async with models.SessionLocal() as db_:
        stmt = select(models.User).filter(models.User.email == email)
        return (await db_.execute(stmt)).scalars().first()


async def create_user(user: schemas.UserCreate):
    async with models.SessionLocal() as db_:
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
        db_.add(db_user)
        await db_.commit()
        return schemas.UserBase(email=db_user.email)


async def create_user_item(item: schemas.ItemCreate, user_id: int):
    async with models.SessionLocal() as db_:
        db_item = models.Item(**item.dict(), owner_id=user_id)
        db_.add(db_item)
        await db_.commit()
        return db_item


async def subscribe_user(user1: models.User, user2: models.User):
    async with models.SessionLocal() as db_:
        subs = models.UserSubs()
        subs.subscriber = user1
        subs.subscription = user2
        db_.add(subs)
        await db_.commit()


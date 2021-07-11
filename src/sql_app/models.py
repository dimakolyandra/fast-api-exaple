import os
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DB_CONNECT_STRING")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_size=450, max_overflow=30)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


class UserSubs(Base):
    __tablename__ = 'user_subs'
    subscriber_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    subscribe_to_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    subscriber = relationship("User", back_populates="subscriptions", foreign_keys=[subscriber_id])
    subscription = relationship("User", back_populates="subscribers", foreign_keys=[subscribe_to_id])


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner", lazy="joined")
    subscriptions = relationship(
        "UserSubs",
        back_populates="subscriber",
        primaryjoin=(UserSubs.subscriber_id == id),
    )
    subscribers = relationship(
        "UserSubs",
        back_populates="subscription",
        primaryjoin=(UserSubs.subscribe_to_id == id),
    )


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items", lazy="joined")

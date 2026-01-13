from collections.abc import AsyncGenerator
import uuid
from datetime import datetime
from sqlalchemy import Column , Text , String , DateTime , ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine ,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase , relationship
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase , SQLAlchemyBaseUserTableUUID
#database url - thats where the database is stored
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass

# create a model of user
class User(SQLAlchemyBaseUserTableUUID, Base):
    posts = relationship("Post", back_populates="user") #means that the user can have multiple posts

#create a model of post
class Post(Base):
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id") , nullable=False)
    caption = Column(Text)
    url = Column(Text,nullable=False)
    file_type = Column(Text,nullable=False)
    file_name = Column(Text,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="posts") #means that the post can have one user

#now we will create a database engine

engine = create_async_engine(DATABASE_URL)

#now we will create a sessionmaker
async_session = async_sessionmaker(engine, expire_on_commit=False)

#now we will create a function to create the database and tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

#now we will create a function to get a session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

#now we will create a function to get a user database
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    # means that we will use the session that we created in the db.py file and yield it to the user database 
    yield SQLAlchemyUserDatabase(session, User) 
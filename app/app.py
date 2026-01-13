from sys import prefix
from fastapi import FastAPI , HTTPException , File , UploadFile , Form , Depends
from app.schemas import PostCreate , PostResponse , UserRead , UserCreate , UserUpdate
from app.db import create_db_and_tables , get_async_session , Post
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select 
from app.images import imagekit
import os
import uuid
import tempfile
import shutil 

from app.users import auth_backend , current_active_user , fastapi_users

@asynccontextmanager #means that this function will be used as a context manager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan) # Create FastAPI instance

#authentication router 
app.include_router(fastapi_users.get_auth_router(auth_backend),prefix='/auth/jwt',tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead,UserCreate),prefix='/auth/jwt',tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(),prefix='/auth',tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead),prefix='/auth',tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead,UserUpdate),prefix='/auth',tags=["auth"])

#upload endpoint for upload file

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption : str = Form(...),
    session: AsyncSession = Depends(get_async_session) # dependency injection means that we will use the session that we created in the db.py file
):

    temp_file_path = None
    try :
        with tempfile.NamedTemporaryFile(delete=False , suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file , temp_file)
        
        upload_result = imagekit.files.upload(
            file = open(temp_file_path , "rb"),
            file_name = file.filename,
            use_unique_file_name = True,
            tags = ["backend-upload"]
        )
        if upload_result:         
            post = Post(
                caption=caption,
                url=upload_result.url,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name,

            )
            session.add(post) #means add the post to the session (db)
            await session.commit() # means commit the session (db)
            await session.refresh(post) # means refresh the post (db)
            return post
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))
    finally:
        if temp_file_path or os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()


@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]
    posts_data =[]
    for post in posts:
        posts_data.append({
            "id": str(post.id),
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at.isoformat()
        })
    return {"posts": posts_data}

@app.delete("/delete/{post_id}")
async def delete_post(post_id: str , session: AsyncSession = Depends(get_async_session)): #means that we will use the session that we created in the db.py file
    try :
        post_id = uuid.UUID(post_id)
        query = select(Post).where(Post.id == post_id)
        result = await session.execute(query)
        post = result.scalars().first() #means get the first post
        if not post:
            raise HTTPException(status_code=404 , detail="Post not found")
        await session.delete(post) #means delete the post
        await session.commit() # means commit the session (db)
        return {
            "success": True,
            "message": "Post deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))
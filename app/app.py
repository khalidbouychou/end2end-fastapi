from fastapi import FastAPI , HTTPException

app = FastAPI() # Create FastAPI instance

text_post = {
    1: {
        "title": "First Post",
        "content": "This is the content of the first post."
    },
    2: {
        "title": "Second Post",
        "content": "This is the content of the second post."
    },
    3: {
        "title": "Third Post",
        "content": "This is the content of the third post."
    },
    4: {
        "title": "Fourth Post",
        "content": "This is the content of the fourth post."
    },
    5: {
        "title": "Fifth Post",
        "content": "This is the content of the fifth post."
    },
    6: {
        "title": "Sixth Post",
        "content": "This is the content of the sixth post."
    },
    7: {
        "title": "Seventh Post",
        "content": "This is the content of the seventh post."
    },
    8: {
        "title": "Eighth Post",
        "content": "This is the content of the eighth post."
    },
    9: {
        "title": "Ninth Post",
        "content": "This is the content of the ninth post."
    },
    10: {
        "title": "Tenth Post",
        "content": "This is the content of the tenth post."
    }
}


# @app.get("/posts")
# def get_posts():
#     return {"data": text_post}

@app.get("/posts")
def get_posts(limit:int=None):
    if limit:
        return list(text_post.values())[:limit]
    return text_post

@app.get("/posts/{id}")
def getpost(id:int):
    if id not in text_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_post.get(id)


@app.post("/posts")
def create_post():
    return {"message": "Post created successfully"}

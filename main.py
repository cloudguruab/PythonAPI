from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    """Defines schema of what client should send to the server"""
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None 

@app.get('/')
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "this is a post"}

@app.post("/create_posts")
def create_posts(new_post: Post):
    return {"data": "new post"} 


from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor #due to normal cursor not returning column names
import psycopg2
import os

load_dotenv()

try: 
    conn=psycopg2.connect(
        host='localhost',
        database='fastapi',
        user='postgres',
        password=os.environ.get('PASS'),
        cursor_factory=RealDictCursor
    ) 
    cursor = conn.cursor()
    print("db connection resolved")
except Exception as e:
    print("db connection failed", e)
    
app = FastAPI()

class Post(BaseModel):
    """Defines schema of what client should send to the server"""
    title: str
    content: str
    published: bool = True


@app.get('/') 
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/create_posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get(f"/posts/{id}")
def get_post(id):
    print(f'{id}')
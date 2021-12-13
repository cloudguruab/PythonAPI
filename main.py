from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor #due to normal cursor not returning column names
from sqlalchemy.orm import Session
import models

app = FastAPI()
models.Base.metadata.create_all(bind=models.engine)


class Post(BaseModel):
    """Defines schema of what client should send to the server"""
    title: str
    content: str
    published: bool = True

@app.get("/posts")
def get_posts(db: Session = Depends(models.get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/create_posts")
def create_posts(post: Post, db: Session = Depends(models.get_db)):
    new_post = models.Post(
        **post.dict()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get(f"/posts/{id}")
def get_post(id: int, db: Session = Depends(models.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not found')
    
    return {'post detail': post}

@app.delete(f"/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(models.get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not found')
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put(f'posts/{id}')
def update_post(id: int, updated_post: Post, db: Session = Depends(models.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post {id} not found')
    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return {'data': post.first()}
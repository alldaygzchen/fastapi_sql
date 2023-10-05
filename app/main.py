from typing import Optional,List
from fastapi import Depends,FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import Random
from sqlalchemy.orm import Session

from . import models,schema
from .database import engine,get_db



models.Base.metadata.create_all(bind=engine) #create table


app = FastAPI()


@app.get("/")
def root():
    return {"message":"Hello world"}

# @app.get("/sqlalchemy")
# def test(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data":posts}

@app.get("/posts",response_model= List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}",response_model= schema.Post)
def get_posts(id:int,db: Session = Depends(get_db)):
    post=  db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="nothing")
    return post


@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model= schema.Post)
def create_posts(post:schema.PostCreate,db: Session = Depends(get_db)):
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db: Session = Depends(get_db)):

    deleted_post = db.query(models.Post).filter(models.Post.id==id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="nothing")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",response_model= schema.Post)
def update_posts(id:int,updated_post:schema.PostCreate,db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="nothing")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()


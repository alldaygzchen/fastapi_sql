from typing import List,Optional
from fastapi import Depends,Response,status,HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models,schema, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model= List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}",response_model= schema.PostOut)
def get_posts(id:int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="nothing")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
    return post


@router.post("/",status_code=status.HTTP_201_CREATED,response_model= schema.Post)
def create_posts(post:schema.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    deleted_post_query = db.query(models.Post).filter(models.Post.id==id)
    deleted_post = deleted_post_query.first() 

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="nothing")
    
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model= schema.Post)
def update_posts(id:int,updated_post:schema.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="nothing")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
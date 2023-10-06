from fastapi import Depends,FastAPI,status,HTTPException
from sqlalchemy.orm import Session

from . import models,schema,utils
from .database import engine,get_db
from fastapi.middleware.cors import CORSMiddleware
from .routers import post,user,auth

models.Base.metadata.create_all(bind=engine) #create table


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message":"Hello world"}

# @app.get("/sqlalchemy")
# def test(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data":posts}




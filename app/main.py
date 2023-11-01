from fastapi import Depends,FastAPI
from . import models
from .database import engine,get_db
from fastapi.middleware.cors import CORSMiddleware
from .routers import post,user,auth, vote
from .config import settings
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# models.Base.metadata.create_all(bind=engine) #create table


app = FastAPI()
security = HTTPBasic()
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
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message":"Hello world"}

# @app.get("/sqlalchemy")
# def test(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data":posts}

@app.get("/get_ad_username")
async def get_ad_username(credentials: HTTPBasicCredentials = security):
    ad_username = credentials.username
    return {"ad_username": ad_username}
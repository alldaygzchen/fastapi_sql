from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import Random
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool =True

while True:
    try:
        conn =psycopg2.connect(
            host='localhost',
            database='fastapi',user='postgres',password='gonzalo0000',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Success')
        break
    except Exception as error:
        print('Failed',str(error))
        time.sleep(2)

@app.get("/")
def root():
    return {"message":"Hello world"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.get("/posts/{id}")
def get_posts(id:int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="nothing")
    return {"data":post}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute(
        """INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
        (post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int):
    cursor.execute(
        """DELETE FROM posts WHERE id= %s returning * """,(str(id),))
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="nothing")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_posts(id:int,post:Post):
    cursor.execute(
        """UPDATE posts SET title = %s,content=%s,published=%s WHERE id =%s RETURNING *""",(post.title,post.content,post.published,str(id),))
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="nothing")
    conn.commit()
    return {"data":updated_post}


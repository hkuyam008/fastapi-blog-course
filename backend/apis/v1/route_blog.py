from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.blog import CreateBlog,ShowBlog, UpdateBlog
from db.repository.blog import create_new_blog, retrieve_blog, list_blogs, update_blog_by_id, delete_blog_by_id
from typing import List, Dict


router = APIRouter()

@router.post("/", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
def create_blog(blog: CreateBlog, db: Session = Depends(get_db)):
    blog = create_new_blog(blog=blog, db=db, author_id=1)
    return blog

@router.get("/{id}", response_model=ShowBlog)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = retrieve_blog(id=id, db=db)
    if not blog:
        raise HTTPException(detail=f"Blog with id {id} not found", status_code=status.HTTP_404_NOT_FOUND)
    return blog

@router.get("/", response_model=List[ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = list_blogs(db)
    if blogs.count() == 0:
        raise HTTPException(detail="No blogs found", status_code=status.HTTP_404_NOT_FOUND)
    return blogs

@router.put("/{id}", response_model=ShowBlog)
def update_blog(id: int, blog: UpdateBlog, db: Session = Depends(get_db)):
    blog = update_blog_by_id(id=id, blog=blog, db=db, author_id=1)
    if not blog:
        raise HTTPException(detail=f"Blog with id {id} not found!", status_code=status.HTTP_404_NOT_FOUND)
    return blog

@router.delete("/{id}", response_model=Dict[str, str])
def delete_blog(id: int, db: Session=Depends(get_db)):
    message = delete_blog_by_id(id=id, db=db, author_id=1)
    if message.get("error"):
        raise HTTPException(detail=message.get("error"), status_code=status.HTTP_400_BAD_REQUEST)
    return message
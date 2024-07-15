from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from db.repository.blog import list_blogs, retrieve_blog
from db.session import get_db

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/")
def home(request: Request, alert :Optional[str] = None, db: Session = Depends(get_db)):
    blogs = list_blogs(db)
    context = {"request": request, "blogs": blogs, "alert": alert}
    return templates.TemplateResponse("blogs/home.html", context=context)

@router.get("/app/blog/{id}")
def blog_detail(request: Request, id:str, db:Session = Depends(get_db)):
    blog = retrieve_blog(id=id, db=db)
    context = {"request": request, "blog": blog}
    return templates.TemplateResponse("blogs/detail.html", context=context)

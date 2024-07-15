import json
from fastapi import APIRouter, Request, Depends, responses, status, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic.error_wrappers import ValidationError

from db.session import get_db
from schemas.user import UserCreate
from db.repository.user import create_new_user
from apis.v1.route_login import authenticate_user
from core.security import create_access_token


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register")
def register(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    errors = []
    try:
        user = UserCreate(email=email, password=password)
        create_new_user(user=user, db=db)
        return responses.RedirectResponse("/?alert=Successfully%20Registered", status_code=status.HTTP_302_FOUND)
    except ValidationError as e:
        errors_list = json.loads(e.json())
        for item in errors_list:
            errors.append(item.get("loc")[0]+": "+item.get("msg"))
        return templates.TemplateResponse("auth/register.html", {"request": request, "errors": errors})


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
def login(request: Request, email:str = Form(...), password:str = Form(...), db: Session = Depends(get_db)):
    errors = []
    try:
        user = authenticate_user(email=email, password=password, db=db)
        if not user:
            errors.append("Incorrect email or password")
            return templates.TemplateResponse("auth/login.html", {"request": request, "errors": errors, "email": email, "password": password})
        
        access_token = create_access_token({"sub": email})
        response =  responses.RedirectResponse("/?alert=Successfully%20Logged%20in", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token", value="Bearer "+ access_token)
        return response
    except:
        pass
    
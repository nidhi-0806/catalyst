import shutil
from datetime import timedelta
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pathlib import Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .auth import get_current_user
from .database import get_db
from . import crud, schemas

from . import models, schemas, crud, auth, database, celery_worker
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request, current_user: schemas.User = Depends(get_current_user)):
    return templates.TemplateResponse("upload.html", {"request": request, "user": current_user})

@app.get("/query", response_class=HTMLResponse)
async def query_page(request: Request, current_user: schemas.User = Depends(get_current_user)):
    return templates.TemplateResponse("query.html", {"request": request, "user": current_user})

@app.get("/manage", response_class=HTMLResponse)
async def manage_page(request: Request, current_user: schemas.User = Depends(get_current_user)):
    return templates.TemplateResponse("manage.html", {"request": request, "user": current_user})


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response = RedirectResponse(url="/upload", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@app.post("/users/")
async def create_user(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = schemas.UserCreate(email=email, password=password)
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_user(db=db, user=user)
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    file_location = f"/path/to/store/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    celery_worker.process_csv.delay(file_location, current_user.id)
    return {"info": "File uploaded successfully"}

@app.get("/csv_records/", response_model=List[schemas.CSVRecord])
def read_csv_records(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    records = crud.get_csv_records(db, user_id=current_user.id)
    return records

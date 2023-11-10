from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas
import models
import utils
import os
import shutil


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()

origins = [
    "http://localhost:8080", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOADS_DIR = "uploads"


os.makedirs(UPLOADS_DIR, exist_ok=True)

@app.post('/register')
async def register_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(models.User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = utils.get_hashed_password(user.password)

    new_user = models.User(username=user.username, email=user.email, password=encrypted_password )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message":"user created successfully"}

@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOADS_DIR, file.filename)

    with open(file_path, "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)

    return {"filename": file.filename, "saved_path": file_path}





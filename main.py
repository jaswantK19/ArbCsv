from operator import and_

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal
from auth_bearer import JWTBearer
import schemas
from schemas import UpdatedCSV
import datetime
import models
import utils
import os
import jwt
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

    new_user = models.User(username=user.username, email=user.email, password=encrypted_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "user created successfully"}


@app.get('/users/{user_id}')
def get_username(user_id: int, db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return user.username


@app.post('/login', response_model=schemas.TokenSchema)
def login(request: schemas.LoginRequest, db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.password
    if not utils.verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    access = utils.create_access_token(user.user_id)
    refresh = utils.create_refresh_token(user.user_id)

    token_db = models.TokenTable(user_id=user.user_id, access_token=access, refresh_token=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }


@app.post('/logout')
def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_session)):
    token = dependencies
    payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), "HS256")
    user_id = payload['sub']
    token_record = db.query(models.TokenTable).all()
    info = []
    for record in token_record:
        print("record", record)
        if (datetime.datetime.utcnow() - record.created_date).days > 1:
            info.append(record.user_id)
    if info:
        existing_token = db.query(models.TokenTable).where(models.TokenTable.user_id.in_(info)).delete()
        db.commit()

    existing_token = db.query(models.TokenTable).filter(models.TokenTable.user_id == user_id,
                                                        models.TokenTable.access_token == token).first()
    if existing_token:
        existing_token.status = False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)
    return {"message": "Logout Successfully"}


def get_current_user(db: Session = Depends(get_session), token=Depends(JWTBearer())):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not authorized",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), "HS256")
        user_id = payload['sub']

    except:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...), current_user: models.User = Depends(get_current_user),
                             db: Session = Depends(get_session)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not Authenticated"
        )

    user_folder = str(current_user.user_id)
    user_upload_dir = os.path.join(UPLOADS_DIR, user_folder)

    if not os.path.exists(user_upload_dir):
        os.makedirs(user_upload_dir)

    file_path = os.path.join(user_upload_dir, file.filename)

    with open(file_path, "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)

    db_upload = models.Uploads(name=file.filename, src=file_path, user_id=current_user.user_id)
    db.add(db_upload)
    db.commit()
    db.refresh(db_upload)
    return {"filename": file.filename, "saved_path": file_path}
@app.get('/getUploads', response_model=None)
async def get_uploads(db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )
    uploads = db.query(models.Uploads).filter(models.Uploads.user_id == current_user.user_id).all()
    return uploads

@app.get('/viewFile/{upload_id}')
async def view_file(upload_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access"
        )
    file_record = db.query(models.Uploads).filter(and_(models.Uploads.upload_id == upload_id,
                                                    models.Uploads.user_id == current_user.user_id)).first()

    if not file_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

        # Construct the file path
    file_path = file_record.src

    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    # Open the file and read its content
    with open(file_path, 'rb') as file:
        file_content = file.read()

    # Return the file content as a StreamingResponse
    return StreamingResponse(
        iter([file_content]),
        media_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{os.path.basename(file_path)}"'}
    )


@app.put('/updateFile/{upload_id}')
async def update_file(upload_id: int, updated_csv: UpdatedCSV):
    # Logic to update the file with ID `upload_id`
    # For simplicity, let's assume the updated CSV data is received as a string

    # Retrieve the file path based on upload_id from your database
    # Update the file content with the received data
    file_path = f'/path/to/your/files/{upload_id}.csv'  # Replace this with your file path logic
    try:
        with open(file_path, 'w') as file:
            file.write(updated_csv.data)
        return {"message": "File updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update file: {str(e)}")
@app.delete('/delete/{upload_id}')
def delete_file(upload_id: int, db: Session = Depends(get_session)):
    fileItem = db.get(models.Uploads, upload_id)
    if not fileItem:
        raise HTTPException(status_code=404, detail='File Not Found')
    db.delete(fileItem)
    db.commit()
    return {"Message": "Delete Successful"}

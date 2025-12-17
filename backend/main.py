import os
import shutil
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

# App Setup
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./posts.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    type = Column(String)  # text, image, video
    media_path = Column(String, nullable=True)
    status = Column(String, default="draft") # draft, scheduled, posted

class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    reddit_client_id = Column(String, nullable=True)
    reddit_client_secret = Column(String, nullable=True)
    reddit_username = Column(String, nullable=True)
    reddit_password = Column(String, nullable=True)
    reddit_default_subreddit = Column(String, nullable=True)
    twitter_username = Column(String, nullable=True)
    twitter_password = Column(String, nullable=True)
    twitter_email = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

# Media Directory
MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

# Routes
@app.post("/posts/")
async def create_post(
    title: str = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    media: Optional[UploadFile] = File(None)
):
    db = SessionLocal()
    try:
        media_path = None
        if media:
            # Generate unique filename
            file_extension = os.path.splitext(media.filename)[1]
            filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(MEDIA_DIR, filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(media.file, buffer)
            
            media_path = file_path

        new_post = Post(
            title=title,
            description=description,
            type=type,
            media_path=media_path
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/posts/")
def read_posts():
    db = SessionLocal()
    posts = db.query(Post).all()
    db.close()
    return posts

class SettingsSchema(BaseModel):
    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    reddit_username: Optional[str] = None
    reddit_password: Optional[str] = None
    reddit_default_subreddit: Optional[str] = None
    twitter_username: Optional[str] = None
    twitter_password: Optional[str] = None
    twitter_email: Optional[str] = None

@app.get("/settings/")
def get_settings():
    db = SessionLocal()
    settings = db.query(Settings).first()
    if not settings:
        settings = Settings()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    db.close()
    return settings

@app.post("/settings/")
def update_settings(config: SettingsSchema):
    db = SessionLocal()
    settings = db.query(Settings).first()
    if not settings:
        settings = Settings()
        db.add(settings)
    
    for var, value in vars(config).items():
        if value is not None:
            setattr(settings, var, value)
            
    db.commit()
    db.refresh(settings)
    db.close()
    return settings

class RedditConfig(BaseModel):
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    subreddit: Optional[str] = None

@app.post("/publish/reddit/{post_id}")
def publish_to_reddit(post_id: int, config: RedditConfig):
    db = SessionLocal()
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        db.close()
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Resolve credentials
    settings = db.query(Settings).first()
    
    c_id = config.client_id or (settings.reddit_client_id if settings else None)
    c_secret = config.client_secret or (settings.reddit_client_secret if settings else None)
    u_name = config.username or (settings.reddit_username if settings else None)
    pwd = config.password or (settings.reddit_password if settings else None)
    sub = config.subreddit or (settings.reddit_default_subreddit if settings else None)
    
    if not all([c_id, c_secret, u_name, pwd, sub]):
        db.close()
        raise HTTPException(status_code=400, detail="Missing Reddit credentials. Please check Settings.")

    try:
        from automation.reddit_poster import RedditPoster
        poster = RedditPoster(
            client_id=c_id,
            client_secret=c_secret,
            username=u_name,
            password=pwd
        )
        
        permalink = ""
        if post.type == "text":
            permalink = poster.post_text(sub, post.title, post.description)
        elif post.type == "image" and post.media_path:
            # Ensure absolute path
            abs_path = os.path.abspath(post.media_path)
            permalink = poster.post_image(sub, post.title, abs_path)
        elif post.type == "video" and post.media_path:
            abs_path = os.path.abspath(post.media_path)
            permalink = poster.post_video(sub, post.title, abs_path)
        
        post.status = "posted_reddit"
        db.commit()
        db.close()
        return {"status": "success", "permalink": permalink}
        
    except Exception as e:
        db.close()
        raise HTTPException(status_code=500, detail=str(e))

class TwitterConfig(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None

@app.post("/publish/twitter/{post_id}")
def publish_to_twitter(post_id: int, config: TwitterConfig):
    db = SessionLocal()
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        db.close()
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Resolve credentials
    settings = db.query(Settings).first()
    
    u_name = config.username or (settings.twitter_username if settings else None)
    pwd = config.password or (settings.twitter_password if settings else None)
    email = config.email or (settings.twitter_email if settings else None)
    
    if not u_name or not pwd:
        db.close()
        raise HTTPException(status_code=400, detail="Missing X (Twitter) credentials. Please check Settings.")

    try:
        from automation.twitter_poster import TwitterPoster
        poster = TwitterPoster(
            username=u_name,
            password=pwd,
            email=email
        )
        
        poster.login()
        
        media_path = None
        if post.media_path:
            media_path = os.path.abspath(post.media_path)
            
        poster.post(f"{post.title}\n\n{post.description}", media_path)
        
        post.status = "posted_twitter"
        db.commit()
        db.close()
        return {"status": "success"}
        
    except Exception as e:
        db.close()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from sqlalchemy import (Column, Integer, String,
                        Boolean, TIMESTAMP, create_engine,
                        text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.environ.get('URL') #TODO: docs

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        print('DB connection success')
        yield db
    finally:
        db.close()
        
class Post(Base):
    
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
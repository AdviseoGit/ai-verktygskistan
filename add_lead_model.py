import sys
import os
sys.path.append(os.getcwd())

from sqlalchemy import Column, Integer, String, DateTime
from database import Base, engine
import datetime

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)
print("Lead table created.")

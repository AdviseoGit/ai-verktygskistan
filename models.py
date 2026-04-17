from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(Text)
    pricing = Column(String)
    rating = Column(Float)
    gdpr_status = Column(String)
    tags = Column(String)  # comma separated
    icon_emoji = Column(String)
    icon_bg_color = Column(String)

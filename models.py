from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from database import Base
import datetime

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

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class NewsletterSubscriber(Base):
    """Prenumeranter på "Veckans AI-verktyg"."""
    __tablename__ = "newsletter_subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String)       # vilken yrkesroll de valt, för segmentering
    source = Column(String)     # vilken sida anmälan kom från
    confirmed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class B2BLead(Base):
    """Företag som vill ha hjälp att införa AI – säljs vidare eller följs upp."""
    __tablename__ = "b2b_leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    company = Column(String)
    role = Column(String)
    employees = Column(String)
    need = Column(Text)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class CalcData(Base):
    __tablename__ = "calc_data"

    id = Column(Integer, primary_key=True, index=True)
    employees = Column(Integer)
    salary = Column(Integer)
    industry = Column(String)
    saved_value = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

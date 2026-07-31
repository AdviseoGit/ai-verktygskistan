import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Databasen MÅSTE ligga på en Railway-volym. Containerns filsystem är flyktigt
# och sajten deployas i princip dagligen av site-driver-cronen — låg databasen
# kvar på ./tools.db nollställdes alla leads vid varje deploy (2026-07-29:
# samtliga tabeller stod på 0 rader trots inkomna anmälningar).
#
# Sökvägen sätts med DATABASE_URL i Railway (t.ex. sqlite:////data/tools.db) så
# att konfigurationen lever i miljön, inte i koden. Fallbacken är kvar för lokal
# körning.
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./tools.db")

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

if SQLALCHEMY_DATABASE_URL.startswith("sqlite:////"):
    # skapa monteringskatalogen om volymen är tom vid första start
    os.makedirs(os.path.dirname(SQLALCHEMY_DATABASE_URL[len("sqlite:///"):]), exist_ok=True)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

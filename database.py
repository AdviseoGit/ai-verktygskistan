"""Databasanslutning.

Styrs av `DATABASE_URL`. Två uppsättningar som fungerar i produktion:

* `sqlite:////data/tools.db` – SQLite på en monterad Railway-volym.
* `postgresql://…`           – hostad Postgres, med automatiska säkerhetskopior.

Det som **inte** fungerar är en relativ SQLite-sökväg som `sqlite:///./tools.db`.
Den hamnar på containerns filsystem, och eftersom tjänsten deployas i praktiken
dagligen av site-driver-cronen återskapades filen tom ungefär var 24:e timme.
Den 29 juli 2026 stod samtliga tabeller på noll rader trots inkomna anmälningar.
Startloggen varnar därför när den sökvägen används utanför utvecklingsmiljön.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DEFAULT_SQLITE_URL = "sqlite:///./tools.db"


def _normalize(url: str) -> str:
    """Gör om leverantörs-URL:er till en form SQLAlchemy kan använda.

    Railway och Heroku exponerar historiskt `postgres://`, ett schema
    SQLAlchemy slutade acceptera i 1.4. Vi kör psycopg 3, som kräver att
    drivrutinen anges explicit i schemat.
    """
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


SQLALCHEMY_DATABASE_URL = _normalize(
    os.environ.get("DATABASE_URL", "").strip() or DEFAULT_SQLITE_URL
)

IS_SQLITE = SQLALCHEMY_DATABASE_URL.startswith("sqlite")
# Fyra snedstreck betyder absolut sökväg, alltså en monterad volym. Tre betyder
# relativ sökväg – den ligger på containerdisken och överlever inte en deploy.
IS_EPHEMERAL_SQLITE = IS_SQLITE and not SQLALCHEMY_DATABASE_URL.startswith("sqlite:////")

if IS_SQLITE:
    if not IS_EPHEMERAL_SQLITE:
        # Skapa monteringskatalogen om volymen är tom vid första start.
        db_path = SQLALCHEMY_DATABASE_URL[len("sqlite:///"):]
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    else:
        print("[db] VARNING: kör mot en relativ SQLite-sökväg. Lokalt är det "
              "väntat – i produktion raderas all data vid nästa deploy. Sätt "
              "DATABASE_URL till sqlite:////data/tools.db (volym) eller till "
              "en Postgres-instans.")
    engine = create_engine(SQLALCHEMY_DATABASE_URL,
                           connect_args={"check_same_thread": False})
else:
    # pool_pre_ping fångar anslutningar som databasen redan hunnit stänga,
    # vilket är vanligt på hostade instanser mellan trafiktoppar.
    engine = create_engine(SQLALCHEMY_DATABASE_URL,
                           pool_pre_ping=True, pool_recycle=300)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

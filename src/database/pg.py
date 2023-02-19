# Connection to PostgreSQL Database

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import Config

pg_engine = create_engine(Config.POSTGRES_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pg_engine)

Base = declarative_base()

PG = SessionLocal()
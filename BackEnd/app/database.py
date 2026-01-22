from sqlmodel import SQLModel, Session, create_engine, select
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from .models import User

# Use SQLite for local dev (easy, file-based)
DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    with Session(engine) as session:
        yield session
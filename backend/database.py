from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")  # default PostgreSQL port
DB_NAME = os.getenv("DB_NAME")

# Async Database URL for PostgreSQL (asyncpg driver)
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create async engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=True,        # SQL logs, set False in production
    pool_size=5,
    max_overflow=10,
    future=True
)

# Async session factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Base class for models
Base = declarative_base()

# FastAPI dependency
@asynccontextmanager
async def get_db():
    async with SessionLocal() as session:
        yield session

# Optional: Initialize tables on startup
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

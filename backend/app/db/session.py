# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# import os

# DATABASE_URL = os.getenv("DATABASE_URL")

# # Async engine
# engine = create_async_engine(
#     DATABASE_URL,
#     echo=True  # Debugging ke liye
# )

# # Async session factory
# AsyncSessionLocal = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )

# # Dependency for FastAPI
# async def get_session() -> AsyncSession:
#     async with AsyncSessionLocal() as session:
#         yield session

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import asyncio
import asyncpg
import ssl

# SSL context for Neon
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE  # Optional, but Neon usually needs

engine = create_async_engine(
    settings.DATABASE_URL.replace("?sslmode=require", ""),
    echo=True,
    future=True,
    connect_args={"ssl": ssl_context}  # Pass SSL explicitly
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


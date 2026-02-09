# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import ValidationError

# from app.api.routes import auth, todos, chat
# from app.core.config import settings
# from app.db.session import engine
# from app.models.user import User
# from app.models.todo import Todo
# from app.models.conversation import Conversation
# from app.models.message import Message

# from sqlalchemy import text

# app = FastAPI(title=settings.PROJECT_NAME)

# # Set all CORS enabled origins
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#         "http://127.0.0.1:3000",
#         "https://hackathon2-phase3-five.vercel.app",
#         "https://hackathon2-phase2-indol.vercel.app",

#     ] + settings.BACKEND_CORS_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(auth, prefix="/api/auth", tags=["auth"])
# app.include_router(todos, prefix="/api/todos", tags=["todos"])
# app.include_router(chat, prefix="/api/chat", tags=["chat"])

# @app.on_event("startup")
# async def on_startup():
#     async with engine.begin() as conn:
#         # Create tables if they don't exist
#         await conn.run_sync(User.metadata.create_all)
#         await conn.run_sync(Todo.metadata.create_all)
#         await conn.run_sync(Conversation.metadata.create_all)
#         await conn.run_sync(Message.metadata.create_all)
        
#         # Manually add 'name' column if it's missing (since create_all doesn't handle migrations)
#         try:
#             await conn.execute(text('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS name VARCHAR'))
#             await conn.commit()
#         except Exception as e:
#             print(f"Migration note: {e}")

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.routes import auth, todos, chat
from app.core.config import settings
from app.db.session import engine
from app.models.user import User
from app.models.todo import Todo
from app.models.conversation import Conversation
from app.models.message import Message

app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth, prefix="/api/auth", tags=["auth"])
app.include_router(todos, prefix="/api/todos", tags=["todos"])
app.include_router(chat, prefix="/api/chat", tags=["chat"])

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Todo.metadata.create_all)
        await conn.run_sync(Conversation.metadata.create_all)
        await conn.run_sync(Message.metadata.create_all)

        # Add missing 'name' and 'password_hash' columns if not exists
        try:
            await conn.execute(text('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS name VARCHAR'))
            # Drop 'username' column if it exists to resolve NotNullViolationError
            await conn.execute(text('ALTER TABLE "user" DROP COLUMN IF EXISTS username'))
            # Drop 'hashed_password' column if it exists (old schema name)
            await conn.execute(text('ALTER TABLE "user" DROP COLUMN IF EXISTS hashed_password'))
            # Add 'password_hash' column if it doesn't exist (current schema name)
            await conn.execute(text('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS password_hash VARCHAR'))
            await conn.commit()
        except Exception as e:
            print(f"Migration note: {e}")

@app.get("/")
async def root():
    return {"message": "Hello World"}

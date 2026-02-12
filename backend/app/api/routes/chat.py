import json
from uuid import UUID
from datetime import datetime
from typing import Any, List, Optional

import json
from uuid import UUID
from datetime import datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from agents import Runner

from app.api.deps import get_current_user
from app.db.session import async_session # Changed import
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.chat import ChatRequest, ChatResponse, ToolCallSchema
from app.agents.todo_agent import get_todo_agent, get_agent_config

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(
    *,
    # session: AsyncSession = Depends(get_session), # Removed dependency
    chat_in: ChatRequest,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Send a message to the AI agent and get a response.
    """
    messages = []
    conversation_id = chat_in.conversation_id

    # --- Transaction 1: Save user message and fetch history ---
    try:
        async with async_session() as session:
            # 1. Get or Create Conversation
            if not conversation_id:
                conversation = Conversation(user_id=current_user.id)
                session.add(conversation)
                await session.commit()
                await session.refresh(conversation)
                conversation_id = conversation.id
            else:
                result = await session.execute(
                    select(Conversation).where(
                        Conversation.id == conversation_id, 
                        Conversation.user_id == current_user.id
                    )
                )
                conversation = result.scalars().first()
                if not conversation:
                    raise HTTPException(status_code=404, detail="Conversation not found")

            # 2. Save User Message
            user_msg = Message(
                conversation_id=conversation_id,
                role="user",
                content=chat_in.message
            )
            session.add(user_msg)
            await session.commit() # Commit the user message

            # 3. Fetch History
            result = await session.execute(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(20)
            )
            history_msgs = result.scalars().all()
            history_msgs.reverse()

            for msg in history_msgs:
                messages.append({"role": msg.role, "content": msg.content})
    except Exception as e:
        # This part will catch DB errors before the agent call
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # --- Agent Execution (No DB session held) ---
    agent = get_todo_agent(str(current_user.id))
    config = get_agent_config()
    
    try:
        result = await Runner.run(agent, input=messages, run_config=config)
        assistant_content = result.final_output
        
        # --- Transaction 2: Save assistant message ---
        async with async_session() as session:
            assistant_msg = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=assistant_content,
            )
            session.add(assistant_msg)
            await session.commit()

        # --- Return Response ---
        return ChatResponse(
            response=assistant_content,
            conversation_id=conversation_id,
        )
        
    except Exception as e:
        # This will catch errors from the agent or the second DB transaction
        # We don't have a session to rollback here, as it's handled by 'async with'
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

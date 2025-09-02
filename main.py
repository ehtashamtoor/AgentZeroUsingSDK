import asyncio, os, json
import sys

# # ✅ Fix event loop issue on Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import uvicorn

# if __name__ == "__main__":
#     # ✅ THIS GUARD is required on Windows when using multiprocessing / reload
#     uvicorn.run("agent:app", host="127.0.0.1", port=8000, reload=True)


from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from openai.types.responses import ResponseTextDeltaEvent
from agents import AgentUpdatedStreamEvent, Runner
from pydantic import BaseModel
from agent import AgentZero
from supabase_session import SupabaseSession
from typing import AsyncGenerator
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Agent Zero",
    description="An AgentZero API to ask questions about Ehtasham Toor.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/system-health")
async def system_health():
    """Endpoint to check the health of the system"""

    return {"status": "System is online"}


async def stream_agent_response(query: str, uid: str) -> AsyncGenerator[str, None]:
    session = SupabaseSession(session_id=uid)
    try:
        print("⚡ Starting Runner.run_streamed...")
        result = Runner.run_streamed(
            starting_agent=AgentZero,
            input=query,
            session=session,
            max_turns=50,
        )
        print("⚡ Got RunResultStreaming:")

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(
                event.data, ResponseTextDeltaEvent
            ):
                print("👉 Yielding delta:", event.data.delta)
                chunk = event.data.delta
                safe_chunk = json.dumps(chunk)
                yield f"data: {safe_chunk}\n\n"

        print("✅ Finished streaming")
        yield "data: [DONE]\n\n"

    except Exception as e:
        print(f"⚠️ Unexpected error in stream_agent_response: {e}")
        yield f"data: ⚠️ Error: {str(e)}\n\n"


class ChatQueryRequest(BaseModel):
    question: str
    session_id: str


@app.get("/ask-AgentZero", tags=["AgentZero Chat"])
async def chat(
    question: str = Query(..., description="User question"),
    session_id: str = Query(..., description="Chat session ID"),
):
    question = question.strip()
    session_id = session_id.strip()

    print(f"Received question: {question} with session_id: {session_id}")

    if not question:
        return {"error": "Question cannot be empty."}
    if not session_id:
        return {"error": "Session ID cannot be empty."}

    return StreamingResponse(
        stream_agent_response(question, session_id),
        media_type="text/event-stream",
    )


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    PORT = os.getenv("PORT", 8000)
    uvicorn.run("main:app", host=host, port=os.getenv("PORT", 8000), reload=True)

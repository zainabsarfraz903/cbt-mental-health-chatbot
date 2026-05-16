from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(payload: dict):
    return {"reply": "This is a placeholder response."}

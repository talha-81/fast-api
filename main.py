from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import os
import time

app = FastAPI()
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class Conversation(BaseModel):
    id: int
    created_at: str
    user_message: str
    assistant_message: str
    recipient: str
    sender: str
    name: str

def get_conversation() -> List[Conversation]:
    try:
        response = supabase.table('conversationmemories').select('*').order('id', desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversations: {str(e)}")

@app.get("/conversations", response_model=dict)
async def fetch_conversations():
    conversations = get_conversation()
    return {
        "conversations": conversations,
        "last_updated": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    }
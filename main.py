from fastapi import FastAPI, HTTPException
from supabase import create_client
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import os
import time

app = FastAPI()
load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

class Conversation(BaseModel):
    id: int
    created_at: str
    user_message: str
    assistant_message: str
    sender: str
    recipient: str
    name: str

class GroupedConversation(BaseModel):
    sender: str
    name: str
    conversations: List[Conversation]

def fetch_conversations(phone: str = None) -> List[GroupedConversation]:
    query = supabase.table("conversationmemories").select("*").order("created_at",desc=True)
    if phone:
        query = query.eq("sender", phone)
    
    response = query.execute()
    if not response.data:
        raise HTTPException(status_code=404, detail=f"No conversations found{' for ' + phone if phone else ''}")
    
    groups = {}
    for item in response.data:
        sender = item["sender"]
        if sender not in groups:
            groups[sender] = {
                "sender": sender,
                "name": item["name"],
                "conversations": []
            }
        groups[sender]["conversations"].append(Conversation(**item))
    
    return [GroupedConversation(**group) for group in groups.values()]

@app.get("/conversations")
async def get_all_conversations():
    conversations = fetch_conversations()
    senders = [group.sender for group in conversations]
    return {
        "unique_senders": senders,
        "conversations": conversations,
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/conversations/phone/{phone}")
async def get_conversations_by_phone(phone: str):
    conversations = fetch_conversations(phone)
    return {
        "conversations": conversations,
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
    }
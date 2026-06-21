import os
import requests
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ClientTools

AGENT_ID = "agent_2301kvj37mtfejjva4kzpw4fk4x2"
RENDER_BASE = "https://story-catcher-memory.onrender.com"

elevenlabs_client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

def retrieve_memories(message: str, user_id: str = "seth") -> str:
    r = requests.post(f"{RENDER_BASE}/retrieveMemories", json={"message": message, "user_id": user_id})
    return r.json().get("text", "No memories found.")

def add_memories(message: str, user_id: str = "seth") -> str:
    r = requests.post(f"{RENDER_BASE}/addMemories", json={"message": message, "user_id": user_id})
    return r.json().get("text", "Memory saved.")

client_tools = ClientTools()
client_tools.register("retrieveMemories", retrieve_memories)
client_tools.register("addMemories", add_memories)

conversation = Conversation(
    elevenlabs_client,
    AGENT_ID,
    client_tools=client_tools,
    requires_auth=False,
)

conversation.start_session()

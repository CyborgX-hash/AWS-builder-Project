from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant" | "system"
    content: str


class ChatRequest(BaseModel):
    query: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    crop: Optional[str] = None
    growth_stage: Optional[str] = None
    language: Optional[str] = "en"
    conversation_history: Optional[List[ChatMessage]] = None


class AgentTraceStep(BaseModel):
    agent: str
    action: str
    status: str
    summary: str


class ChatResponse(BaseModel):
    response: str
    language: str
    extracted_entities: Dict[str, Any]
    agent_traces: List[AgentTraceStep]
    structured_data: Optional[Dict[str, Any]] = None
    disclaimer: str


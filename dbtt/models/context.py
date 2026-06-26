"""
Context model for DBTT Cognitive Operating System
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class Context(BaseModel):
    """Represents the context of thoughts"""
    id: str = Field(..., description="Unique identifier for the context")
    thought_ids: List[str] = Field(default_factory=list, description="List of thought IDs in this context")
    user_id: str = Field(default="", description="User ID associated with this context")
    session_id: str = Field(default="", description="Session ID for this context")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context metadata")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}

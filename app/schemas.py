from pydantic import BaseModel, AnyUrl, Field
from typing import Optional
from datetime import datetime

class CreateURLRequest(BaseModel):
    url : AnyUrl
    slug : Optional[str] = None

class URLResponse(BaseModel):
    id: int
    url: str
    shortCode: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {
        "from_attributes": True
    } 

class UpdateURLRequest(BaseModel):
    url: AnyUrl


class ClickResponse(BaseModel):
    timestamp: datetime
    userAgent: str=Field(alias="user_agent")
    model_config={
        "from_attributes": True,
        "populate_by)name":True
    }  

class URLStatsResponse(BaseModel):
    id: int
    url:str
    shortCode: str
    createdAt: datetime
    updatedAt: datetime
    accessCount: int
    clicks: list[ClickResponse]

    model_config = {
        "from_attributes": True
    }
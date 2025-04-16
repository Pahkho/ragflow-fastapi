from pydantic import BaseModel
from typing import Optional

class SQLQueryRequest(BaseModel):
    question: str
    agent_id: str

class SQLQueryResponse(BaseModel):
    response: Optional[str] = None
    sql: Optional[str] = None
    status: str = "success"
    message: Optional[str] = None
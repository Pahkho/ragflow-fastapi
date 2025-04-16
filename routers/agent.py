from fastapi import APIRouter, HTTPException
from schemas import SQLQueryRequest, SQLQueryResponse
from services.ragflowService import create_session, query_ragflow

router = APIRouter()

@router.post("/agent", response_model=SQLQueryResponse)
async def completions(request: SQLQueryRequest):

    """将自然语言转换为SQL的API端点"""
    question = request.question
    agent_id = request.agent_id  # 获取传入的agent_id

    try:
        # 1. 创建新会话（传入agent_id参数）
        session_id = await create_session(agent_id)  # 修改这里

        # 2. 发送查询（传入agent_id参数）
        result = await query_ragflow(session_id, agent_id, question)  # 修改这里

        # 3. 构造响应
        return SQLQueryResponse(
            response=result.get("response", ""),
            sql=result.get("sql", "")
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        return SQLQueryResponse(
            status="error",
            message=str(e)
        )
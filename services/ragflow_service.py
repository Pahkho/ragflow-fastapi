import requests
from fastapi import HTTPException
from config import logger, RAGFLOW_BASE_URL, API_KEY

async def create_session(agent_id: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    url = f"{RAGFLOW_BASE_URL}/api/v1/agents/{agent_id}/sessions"
    
    try:
        response = requests.post(url, headers=headers, json={})
        # 新增调试输出，确保获取到正确的字段
        response_data = response.json()
        print(f"sessionID: {response_data.get('data', {}).get('id') }")  # 新增调试输出
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail=f"Failed to create session: {response.text}")
        
        # 根据实际响应结构调整字段路径（示例假设session_id在data字段中）
        return response_data.get('data', {}).get('id')  # 修改字段路径
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Network error: {str(e)}")

async def query_ragflow(session_id: str, agent_id: str, question: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 使用传入的agent_id
    url = f"{RAGFLOW_BASE_URL}/api/v1/agents/{agent_id}/completions"  # 修改这里
    payload = {
        "session_id": session_id,
        "question": question,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        
        # 改进的SQL提取逻辑
        answer_content = response_json.get('data', {}).get('answer', '')
        print(f"answer_content: {answer_content}")  # 新增调试输出
        return {
            "response": "查询成功",
            "sql": answer_content
        }
    except requests.JSONDecodeError as e:
        # logger.error(f"JSON解析失败: {response.text}")
        raise HTTPException(status_code=500, detail="Invalid JSON response")
    except Exception as e:
        logger.error(f"解析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"解析错误: {str(e)}")
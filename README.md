# AI问数FastAPI服务工程

## 项目结构
```tree
FastAPIProject/
├── app.py               # 服务入口文件
├── config.py            # 应用配置（日志/API密钥等）
├── schemas.py           # 数据模型定义
├── services/            # 业务逻辑实现
│   └── ragflow_service.py 
├── routers/             # API路由模块
│   ├── sql.py          # SQL查询路由
│   └── health.py       # 健康检查路由
└── README.md            # 项目文档
```


## 开发流程

### 1. 环境准备

```bash
# 安装依赖（确保已创建requirements.txt）
pip install -r requirements.txt
```


### 2. 启动服务
```bash
python app.py
```
服务访问：
- 📘 交互式文档： http://localhost:5002/docs
- 📙 Redoc文档： http://localhost:5002/redoc

### 3. 开发新接口
#### 3.1 创建数据模型
在 `schemas.py` 中添加Pydantic模型：
```python
from pydantic import BaseModel

class NewRequest(BaseModel):
    """新功能请求参数"""
    param1: str
    param2: int

class NewResponse(BaseModel):
    """新功能响应参数""" 
    result: str
    status: str = "success"
```

### 3.2 添加路由模块
在 `routers` 目录新建文件（例：` routers/new_feature.py` ）：
```python
from fastapi import APIRouter
from schemas import NewRequest, NewResponse
from services import your_service

router = APIRouter(tags=["新功能模块"])

@router.post("/new-endpoint", 
             response_model=NewResponse,
             summary="新功能端点",
             description="实现XX业务逻辑的API端点")
async def new_feature_endpoint(request: NewRequest):
    """端点功能描述"""
    result = await your_service.process_data(request)
    return result
```

### 3.3 实现业务逻辑
在 `services` 目录新建文件（例： `services/new_service.py` ）
```python
from config import logger
from schemas import NewRequest, NewResponse

async def process_data(request: NewRequest):
    """核心业务逻辑处理"""
    try:
        # 实现业务逻辑
        processed_data = f"processed: {request.param1}"
        return NewResponse(result=processed_data)
    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        return NewResponse(status="error", result=str(e))
```
### 3.4 注册路由
在 `app.py` 中添加：
```python
# ...已有代码...
from routers import new_feature

app.include_router(new_feature.router, prefix="/api")
```

## 代码规范
### 1. 分层架构 ：
   
   - 路由层：仅处理HTTP请求/响应
   - 服务层：实现核心业务逻辑
   - 数据层：定义请求/响应模型
### 2. 配置管理 ：
   
   - 所有环境相关配置存放于 config.py
   - 敏感信息建议使用环境变量
```python
import os
API_KEY = os.getenv("RAGFLOW_API_KEY")
   ```
### 3. 异常处理 ：
   
   - 服务层抛出带状态码的HTTPException
   - 路由层进行统一错误捕获
   - 日志记录使用规范：
```python
logger.info("接口请求参数: %s", params)
logger.error("业务处理异常", exc_info=True)
```
## 常用命令
```bash
# 开发模式运行（自动重载）
python app.py

# 生成依赖清单
pip freeze > requirements.txt

# 测试接口（Windows PowerShell）
curl.exe -Method POST -Uri "http://localhost:5002/api/sql_query" `
-Body '{"""question""":"""查询销售数据""", """agent_id""":"""YOUR_AGENT_ID"""}' `
-ContentType "application/json"

```
## 接口文档
本服务自动生成以下两种API文档：

1. 🔍 交互式文档 - 支持在线测试接口
   - 访问地址： http://localhost:5002/docs
2. 📚 Redoc文档 - 提供更美观的文档展示
   - 访问地址： http://localhost:5002/redoc

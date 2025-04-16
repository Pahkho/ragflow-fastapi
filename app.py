from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 初始化核心应用
app = FastAPI(
    title="RagFlow FASTAPI代理",
    description="RagFlow FASTAPI代理服务",
    version="1.0.0",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载路由模块
from routers import agent, health
app.include_router(agent.router, prefix="/api")
app.include_router(health.router)

# 启动服务
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5002, reload=True)
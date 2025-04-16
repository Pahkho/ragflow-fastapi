from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 初始化核心应用
app = FastAPI(
    title="RagFlow SQL查询代理",
    description="简化版SQL查询代理服务",
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
from routers import sql, health
app.include_router(sql.router, prefix="/api")
app.include_router(health.router)

# 启动服务
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5002, reload=True)
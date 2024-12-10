import os
from fastapi import FastAPI, Request
from api import router
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Backend API",
    description="Backend service with sharding support",
    version="1.0.0"
)

# Add metrics instrumentation BEFORE including router
Instrumentator().instrument(app).expose(app)

# Include the router
app.include_router(router, prefix="/api")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Received request: {request.method} {request.url.path}")
    print(f"Base URL: {request.base_url}")
    print(f"Headers: {request.headers}")
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "Backend API is running"}

@app.get("/ping")
async def ping():
    return {"message": "pong"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

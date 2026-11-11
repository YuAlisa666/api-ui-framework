"""本地 mock 接口服务，供接口自动化用例练习。

单独启动（供 requests / Postman 调试）:
    python -m uvicorn mock_api:app --host 127.0.0.1 --port 8765
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="接口自动化练习 Mock 服务")


class LoginReq(BaseModel):
    username: str
    password: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users/{uid}")
def get_user(uid: int):
    if uid == 0:
        raise HTTPException(status_code=404, detail="user not found")
    return {"id": uid, "name": f"user-{uid}", "active": True}


@app.post("/login")
def login(req: LoginReq):
    if req.username == "admin" and req.password == "123456":
        return {"token": "mock-token-123", "role": "admin"}
    raise HTTPException(status_code=401, detail="bad credentials")

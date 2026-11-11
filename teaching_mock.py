# teaching_mock.py  今天照抄即可，不用理解
#mock接口，主要用于教学，模拟一个订单系统的接口
from fastapi import FastAPI
from pydantic import BaseModel
import time, random

app = FastAPI()
ORDERS = {
    1001: {"order_id": 1001, "user": "tester", "amount": 99.5, "status": "paid"},
    1002: {"order_id": 1002, "user": "tester", "amount": 20.0, "status": "created"},
}

class LoginIn(BaseModel):
    user: str
    pwd: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/login")
def login(body: LoginIn):
    if body.user == "tester" and body.pwd == "123456":
        return {"code": 0, "msg": "ok", "data": {"token": "tk-fake-123"}}
    return {"code": 401, "msg": "bad user or pwd", "data": {}}

@app.get("/orders/{order_id}")
def get_order(order_id: int, token: str = ""):
    if token != "tk-fake-123":
        return {"code": 401, "msg": "need token", "data": {}}
    if order_id not in ORDERS:
        return {"code": 404, "msg": "not found", "data": {}}
    return {"code": 0, "msg": "ok", "data": ORDERS[order_id]}

@app.post("/orders")
def create_order(body: dict):
    oid = max(ORDERS) + 1
    ORDERS[oid] = {"order_id": oid, "user": body.get("user", "tester"),
                   "amount": body.get("amount", 0), "status": "created"}
    return {"code": 0, "msg": "ok", "data": ORDERS[oid]}

@app.get("/flaky")
def flaky():
    if random.random() < 0.3:
        return {"code": 500, "msg": "random error", "data": {}}
    time.sleep(0.2)
    return {"code": 0, "msg": "ok", "data": {"note": "sometimes fails"}}
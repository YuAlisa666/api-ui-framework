from framework.client import ApiClient
from framework.tools import retry, timer

BASE = "http://127.0.0.1:8001"

#本函数用于测试获取订单接口，传入 order_id 为 1001，期望返回的订单号为 1001
def test_get_order_ok(client, token):
    r = client.get("/orders/1001", params={"token": token})
    assert r.json()["data"]["order_id"] == 1001

#这里使用了 retry 装饰器，表示如果函数执行失败，会重试 10 次，每次间隔 0.1 秒
@retry(times=10, wait=0.1)
#本函数用于测试 flaky 接口，flaky 接口有时会返回失败，有时会返回成功
def call_flaky(clent):
    r = clent.get("/flaky")
    assert r.json()["code"] == 0
    return r

#本函数用于测试 flaky 接口，使用了 timer 装饰器，表示会打印函数执行时间
def test_flaky_with_retry(client):
    with timer("flaky 用例"):
        call_flaky(client)


import pytest, yaml, pathlib

#本函数用于加载测试数据，返回一个列表，列表中每个元素是一个元组，
# 元组中包含 order_id 和 expect_amount
def load_cases():
    # 本文件在 tests/api/ 下，数据在 tests/data/ 下，需向上一级
    p = pathlib.Path(__file__).parent.parent / "data" / "orders.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    cases = [(c["order_id"], c["expect_amount"]) for c in data["cases"]]
    print(f"测试数据加载完成，共 {len(cases)} 条：{cases}")
    return cases

# 使用 pytest.mark.parametrize 装饰器，参数化测试用例
@pytest.mark.parametrize("order_id, expect_amount", load_cases())
def test_order_amount(client, token, order_id, expect_amount):
    r = client.get(f"/orders/{order_id}", params={"token": token})
    assert r.json()["data"]["amount"] == expect_amount

# ===== D5 新增：四层断言 + 把原始响应贴进 Allure 报告 =====
import jsonschema, allure
from framework.schema import ORDER_SCHEMA

@allure.step("查询订单 {order_id}")
def step_get_order(client, token, order_id):
    return client.get(f"/orders/{order_id}", params={"token": token})

def test_order_full(client, token):
    r = step_get_order(client, token, 1001)
    allure.attach(r.text, name="原始响应",
                  attachment_type=allure.attachment_type.JSON)

    assert r.status_code == 200                    # 第 1 层 HTTP
    body = r.json()
    jsonschema.validate(body, ORDER_SCHEMA)         # 第 2 层 结构
    assert body["code"] == 0                        # 第 3 层 业务码
    assert body["data"]["amount"] > 0               # 第 4 层 业务值
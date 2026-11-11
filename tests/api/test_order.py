from framework.client import ApiClient
from framework.tools import retry, timer

BASE = "http://127.0.0.1:8001"

def test_get_order_ok():
    c = ApiClient(BASE)
    r = c.get("/orders/1001", params={"token": "tk-fake-123"})
    assert r.json()["data"]["order_id"] == 1001

@retry(times=10, wait=0.1)
def call_flaky(c):
    r = c.get("/flaky")
    assert r.json()["code"] == 0
    return r

def test_flaky_with_retry():
    with timer("flaky 用例"):
        call_flaky(ApiClient(BASE))


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
def test_order_amount(order_id, expect_amount):
    c = ApiClient(BASE)
    r = c.get(f"/orders/{order_id}", params={"token": "tk-fake-123"})
    assert r.json()["data"]["amount"] == expect_amount
# conftest.py
import pytest
from framework.client import ApiClient

# pytest 配置文件，定义了测试环境、基础 URL、token 获取和客户端实例化等功能
#本函数用于添加命令行参数 --env，用于指定测试环境，默认值为 local
def pytest_addoption(parser):
    parser.addoption("--env", default="local", help="local / test")

# pytest.fixture(scope="session") 装饰器表示该 fixture 的作用域为整个测试会话，
# 只有在第一次调用时才会执行，之后的调用都会返回同一个实例
@pytest.fixture(scope="session")
#本函数用于获取命令行参数 --env 的值，返回测试环境名称
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
#本函数用于获取基础 URL，根据测试环境返回不同的 URL
def base_url(env):
    return {"local": "http://127.0.0.1:8001",
            "test":  "http://127.0.0.1:8001"}[env]

@pytest.fixture(scope="session")
def token(base_url):
    r = ApiClient(base_url).post("/login",
                                 json={"user": "tester", "pwd": "123456"})
    assert r.json()["code"] == 0
    return r.json()["data"]["token"]

@pytest.fixture
def client(base_url):
    return ApiClient(base_url)
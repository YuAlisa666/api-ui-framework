from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent


@pytest.fixture(scope="session")
def api_client():
    """本地 mock 接口客户端，无需启动服务，CI 里也能稳定跑。"""
    from mock_api import app

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def demo_page_url():
    """离线 UI 练习页，避免用例依赖外网。"""
    return (ROOT / "data" / "demo.html").as_uri()

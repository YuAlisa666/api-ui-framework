# framework/client.py
import requests

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.s = requests.Session()      # 复用连接，也记住 cookie
        self.s.trust_env = False         # 本地 mock 直连，忽略 HTTP_PROXY / NO_PROXY 等环境变量

    def get(self, path, **kwargs):
        kwargs.setdefault("timeout", 5)  # 超时只在这一处写
        url = self.base_url + path
        print(f"[请求] GET {url} {kwargs.get('params', '')}")
        r = self.s.get(url, **kwargs)
        print(f"[响应] {r.status_code} {r.text[:200]}")
        return r

    def post(self, path, **kwargs):
        kwargs.setdefault("timeout", 5)
        url = self.base_url + path
        print(f"[请求] POST {url}")
        r = self.s.post(url, **kwargs)
        print(f"[响应] {r.status_code} {r.text[:200]}")
        return r
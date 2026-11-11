"""Selenium 4 独立示例（不进 pytest 默认用例集，避免 CI 上缺本地浏览器）。

复用 Playwright 下载到 D 盘的 Chrome for Testing + 本地 chromedriver，
因此不需要 Selenium Manager 联网下载驱动。

运行:
    .venv\Scripts\python.exe examples\selenium_demo.py
"""

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

ROOT = Path(__file__).resolve().parents[1]
CHROME = Path(r"D:\TestEnv\Browsers\chromium-1248\chrome-win64\chrome.exe")
DRIVER = Path(r"D:\TestEnv\Drivers\chromedriver.exe")


def bypass_local_proxy():
    """本机代理会把发往 chromedriver 的请求改写成绝对 URL，导致 400 unhandled request。"""
    for key in ("NO_PROXY", "no_proxy"):
        parts = [p.strip() for p in os.environ.get(key, "").split(",") if p.strip()]
        for host in ("localhost", "127.0.0.1", "::1"):
            if host not in parts:
                parts.append(host)
        os.environ[key] = ",".join(parts)


def main():
    bypass_local_proxy()
    options = Options()
    options.binary_location = str(CHROME)
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(executable_path=str(DRIVER)), options=options
    )
    try:
        driver.get((ROOT / "data" / "demo.html").as_uri())
        assert driver.title == "UI 自动化练习页"
        driver.find_element("id", "btn").click()
        assert driver.find_element("id", "result").text == "OK"
        print("Selenium UI OK:", driver.title)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

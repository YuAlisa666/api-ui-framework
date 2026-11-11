import pytest


@pytest.mark.ui
def test_demo_page_interaction(page, demo_page_url):
    """Playwright 驱动本地 Chromium 打开离线页面并完成一次交互。"""
    page.goto(demo_page_url)
    assert page.title() == "UI 自动化练习页"
    assert page.locator("#title").inner_text() == "Hello Playwright"

    page.locator("#btn").click()
    assert page.locator("#result").inner_text() == "OK"


@pytest.mark.ui
def test_demo_page_screenshot(page, demo_page_url):
    page.goto(demo_page_url)
    assert page.screenshot()[:8] == b"\x89PNG\r\n\x1a\n"

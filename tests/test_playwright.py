#!/usr/bin/env python3
"""
Simple Playwright test for web UI
"""

import asyncio
from playwright.async_api import async_playwright

async def test_web_ui():
    """Simple test: page loads and has basic elements"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Load the page
        await page.goto("http://localhost:5000")
        
        # Check title
        title = await page.title()
        assert "Todo App" in title
        
        # Check key elements exist
        add_button = page.locator("button:has-text('Add Task')")
        task_input = page.locator("#taskInput")
        
        assert await add_button.is_visible()
        assert await task_input.is_visible()
        
        await browser.close()
        return True

if __name__ == "__main__":
    result = asyncio.run(test_web_ui())
    print("✅ Simple UI test passed!" if result else "❌ Test failed")

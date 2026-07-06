import asyncio
import os
from flask import Flask, jsonify
from playwright.async_api import async_playwright

app = Flask(__name__)

async def get_gemini_cookie():
    print("[*] מפעיל דפדפן נסתר בתוך Cloud Run...")
    async with async_playwright() as p:
        # הפעלה עם ארגומנטים מיוחדים לעקיפת חסימות בתוך Docker ומכולות ענן
        browser = await p.chromium.launch(
            headless=True, 
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = await context.new_page()
        
        # כניסה לאתר
        await page.goto("https://google.com", timeout=60000)
        await page.wait_for_timeout(5000)
        
        cookies = await context.cookies()
        for cookie in cookies:
            if cookie['name'] == '__Secure-1PSID':
                return cookie['value']
        return None

@app.route('/')
def home():
    return "Cloud Run Bot is running!"

@app.route('/get-token')
def fetch_token():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    token = loop.run_until_complete(get_gemini_cookie())
    loop.close()
    
    if token:
        return jsonify({"status": "success", "token": token})
    return jsonify({"status": "error", "message": "Cookie not found. Needs session auth."}), 404

if __name__ == "__main__":
    # הקצאת הפורט הדינמי שגוגל דורשת
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

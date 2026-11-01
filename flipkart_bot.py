import requests
import time
import json
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# --- CONFIGURATION ---
PRODUCT_URLS = [
    "https://dl.flipkart.com/s/kGnRsvuuuN",
    "https://dl.flipkart.com/s/xXV5CLNNNN",
    "https://dl.flipkart.com/s/x1KlEnNNNN",
    "https://dl.flipkart.com/s/kG28Y2uuuN",
    "https://dl.flipkart.com/s/kGrfNhuuuN"
]

TELEGRAM_BOT_TOKEN = "8821071084:AAHpfzMk68sjfP9s0BuUDy2Jjo5gXklZfGE"
TELEGRAM_CHAT_ID = "1235288153"

BUY_BUTTON_XPATH = "//*[translate(text(), 'BUY NOW', 'buy now')='buy now'] | //span[translate(text(), 'BUY NOW', 'buy now')='buy now']"

def send_telegram_alert(product_url):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    message = (
        "🚨 Flipkart Stock Alert 🚨\n\n"
        "Product is IN STOCK and successfully reached checkout!\n\n"
        f"🔗 **Product Link:**\n{product_url}"
    )
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": message,
        "disable_web_page_preview": False
    }
    try:
        requests.post(api_url, json=payload, timeout=5)
        print("Telegram alert sent successfully!")
    except Exception as e:
        print(f"Failed to send telegram alert: {e}")

def main():
    print("Starting Flipkart Fast Tracker with flipkart.json...")
    
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Chrome version 156 match karne ke liye
    driver

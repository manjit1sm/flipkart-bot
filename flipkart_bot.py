import requests
import time
import json
import os
import traceback
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# --- CONFIGURATION (Updated with your Oppo K14 Plus links) ---
PRODUCT_URLS = [
    "https://www.flipkart.com/oppo-k14-plus-5g-solar-orange-128-gb/p/itm6b2b1016fd57a?pid=MOBHR3ZYZXYQ2GYK&param=327476&BU=Mobile&pageUID=1793506636583",
    "https://www.flipkart.com/oppo-k14-plus-5g-star-white-128-gb/p/itm6b2b1016fd57a?pid=MOBHR3ZYWM7R57PW&marketplace=FLIPKART&lid=LSTMOBHR3ZYWM7R57PWKRABGU&pageUID=1793506636583"
]

TELEGRAM_BOT_TOKEN = "8821071084:AAHpfzMk68sjfP9s0BuUDy2Jjo5gXklZfGE"
TELEGRAM_CHAT_ID = "1235288153"

BUY_BUTTON_XPATH = "//*[translate(text(), 'BUY NOW', 'buy now')='buy now'] | //span[translate(text(), 'BUY NOW', 'buy now')='buy now']"

def send_telegram_alert(product_url):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    message = (
        "🚨 Flipkart Stock Alert (Oppo K14 Plus) 🚨\n\n"
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
    print("Starting Flipkart Fast Tracker with Oppo K14 Plus links...")
    
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Chrome version 156 match karne ke liye
    driver = uc.Chrome(options=options, version_main=156)
    
    # --- COOKIES LOAD KARNE KA STEP ---
    try:
        driver.get("https://www.flipkart.com")
        time.sleep(2)
        
        if os.path.exists("flipkart.json") and os.path.getsize("flipkart.json") > 0:
            with open("flipkart.json", "r") as file:
                content = file.read().strip()
                if content.startswith('['):
                    cookies = json.loads(content)
                    for cookie in cookies:
                        if 'domain' in cookie:
                            if cookie['domain'].startswith('.'):
                                cookie['domain'] = cookie['domain'][1:]
                        try:
                            driver.add_cookie(cookie)
                        except:
                            pass
                else:
                    lines = content.split('\n')
                    for line in lines:
                        if line.startswith('#') or not line.strip():
                            continue
                        parts = line.strip().split('\t')
                        if len(parts) >= 7:
                            domain, flag, path, secure, expiry, name, value = parts[:7]
                            cookie_dict = {
                                'domain': domain,
                                'path': path,
                                'secure': secure.upper() == 'TRUE',
                                'expiry': int(expiry) if expiry.isdigit() else None,
                                'name': name,
                                'value': value
                            }
                            try:
                                driver.add_cookie(cookie_dict)
                            except:
                                pass
            driver.refresh()
            print("Successfully loaded cookies from flipkart.json!")
            time.sleep(3)
        else:
            print("Warning: flipkart.json file is empty or missing.")
    except Exception as e:
        print(f"Could not load cookies: {e}")
    
    print(f"Tracking {len(PRODUCT_URLS)} products continuously...")
    
    while True:
        for url in PRODUCT_URLS:
            try:
                print(f"\nChecking product: {url}")
                driver.get(url)
                time.sleep(2.5)
                
                current_product_url = driver.current_url
                page_before_click = driver.current_url
                
                buy_button = None
                try:
                    buy_button = driver.find_element(By.XPATH, BUY_BUTTON_XPATH)
                except:
                    pass
                
                if buy_button:
                    print(f"Found 'Buy Now' button! Verifying...")
                    driver.execute_script("arguments[0].click();", buy_button)
                    time.sleep(3) 
                    
                    if driver.current_url != page_before_click or "checkout" in driver.current_url.lower() or "viewcart" in driver.current_url.lower():
                        print("Checkout confirmed! Sending Telegram alert...")
                        send_telegram_alert(current_product_url)
                        time.sleep(15)
                    else:
                        print("Clicked, but URL didn't change.")
                else:
                    print("Product Out of Stock. Moving to next product...")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Error checking product {url}: {e}")
                continue
                
        print("\n--- Completed one full round. Waiting 10 seconds for next round ---")
        time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("CRASHED WITH ERROR:")
        traceback.print_exc()

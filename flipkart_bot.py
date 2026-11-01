import requests
import time
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

PRODUCT_URLS = [
    "https://dl.flipkart.com/s/kGnRsvuuuN",
    "https://dl.pykart.com/s/xXV5CLNNNN", # Apna baki links yahan rakh lein
    # ... baki links ...
]

TELEGRAM_BOT_TOKEN = "8821071084:AAHpfzMk68sjfP9s0BuUDy2Jjo5gXklZfGE"
TELEGRAM_CHAT_ID = "1235288153"
BUY_BUTTON_XPATH = "//*[translate(text(), 'BUY NOW', 'buy now')='buy now'] | //span[translate(text(), 'BUY NOW', 'buy now')='buy now']"

def send_telegram_alert(product_url):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    message = f"🚨 Flipkart Stock Alert 🚨\n\nProduct is IN STOCK!\n\n🔗 {product_url}"
    requests.post(api_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message})

def main():
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = uc.Chrome(options=options, version_main=156)
    
    # --- COOKIES LOAD KARNE KA STEP ---
    try:
        driver.get("https://www.flipkart.com")
        time.sleep(2)
        with open("cookies.json", "r") as file:
            cookies = json.load(file)
            for cookie in cookies:
                # Domain match karne ke liye kuch fields clean karni padti hain
                if 'domain' in cookie:
                    if cookie['domain'].startswith('.'):
                        cookie['domain'] = cookie['domain'][1:]
                try:
                    driver.add_cookie(cookie)
                except:
                    pass
        driver.refresh()
        print("Successfully loaded saved cookies/login session!")
        time.sleep(3)
    except Exception as e:
        print(f"Could not load cookies: {e}")

    while True:
        for url in PRODUCT_URLS:
            try:
                driver.get(url)
                time.sleep(2.5)
                page_before = driver.current_url
                
                buy_button = None
                try:
                    buy_button = driver.find_element(By.XPATH, BUY_BUTTON_XPATH)
                except:
                    pass
                
                if buy_button:
                    driver.execute_script("arguments[0].click();", buy_button)
                    time.sleep(3)
                    if driver.current_url != page_before or "checkout" in driver.current_url.lower():
                        send_telegram_alert(url)
                        time.sleep(15)
                time.sleep(1)
            except Exception as e:
                continue
        time.sleep(10)

if __name__ == "__main__":
    main()

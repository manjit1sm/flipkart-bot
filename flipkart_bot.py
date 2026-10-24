import requests
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# --- CONFIGURATION ---
PRODUCT_URLS = [
    "https://www.flipkart.com/oppo-k14-plus-5g-solar-orange-128-gb/p/itm6b2b1016fd57a?pid=MOBHR3ZYZXYQ2GYK&marketplace=FLIPKART&lid=LSTMOBHR3ZYZXYQ2GYKUXH85B&q=k14+plus&fm=organic&pageUID=1791800875860",
    "https://www.flipkart.com/oppo-k14-plus-5g-star-white-128-gb/p/itm6b2b1016fd57a?pid=MOBHR3ZYWM7R57PW&marketplace=FLIPKART&lid=LSTMOBHR3ZYWM7R57PWKRABGU&q=k14+plus&fm=organic&pageUID=1791800875860"
]

TELEGRAM_BOT_TOKEN = "8821071084:AAHpfzMk68sjfP9s0BuUDy2Jjo5gXklZfGE"
TELEGRAM_CHAT_ID = "1235288153"

# Smart Text-Based XPath
BUY_BUTTON_XPATH = "//*[translate(text(), 'BUY NOW', 'buy now')='buy now'] | //span[translate(text(), 'BUY NOW', 'buy now')='buy now']"

def send_telegram_alert(message_text):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": message_text,
        "disable_web_page_preview": False
    }
    try:
        requests.post(api_url, json=payload, timeout=5)
        print("Telegram alert sent successfully!")
    except Exception as e:
        print(f"Failed to send telegram alert: {e}")

def main():
    print("Starting Continuous Flipkart Tracker...")
    
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = uc.Chrome(options=options, version_main=154)
    
    round_count = 1
    
    # Continuous loop taaki rounds chalte rahein
    while True:
        print(f"\n==============================")
        print(f"--- Starting Checking Round {round_count} ---")
        print(f"==============================")
        
        for url in PRODUCT_URLS:
            try:
                print(f"\nChecking product: {url}")
                driver.get(url)
                time.sleep(3)
                
                buy_button = None
                try:
                    buy_button = driver.find_element(By.XPATH, BUY_BUTTON_XPATH)
                except:
                    pass
                
                if buy_button:
                    print("Found 'Buy Now' button! Product is IN STOCK! Sending Telegram alert...")
                    send_telegram_alert(f"🚨 Flipkart Stock Alert!\nOppo K14 Plus is IN STOCK!\n\n🔗 {url}")
                else:
                    print("Product Out of Stock.")
                
                time.sleep(2)
                
            except Exception as e:
                print(f"Error checking product {url}: {e}")
                continue
                
        print(f"\n--- Completed Round {round_count}. Waiting 30 seconds before next round ---")
        round_count += 1
        time.sleep(30) # Agle round se pehle 30 seconds ka gap

if __name__ == "__main__":
    main()

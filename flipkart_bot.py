import requests
import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# --- CONFIGURATION ---
SHORT_URL = "https://dl.flipkart.com/s/CjBCamNNNN"
TELEGRAM_BOT_TOKEN = "8821071084:AAHpfzMk68sjfP9s0BuUDy2Jjo5gXklZfGE"
TELEGRAM_CHAT_ID = "1235288153"

# Smart Text-Based XPath
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
        response = requests.post(api_url, json=payload, timeout=5)
        print("Telegram alert sent successfully!")
    except Exception as e:
        print(f"Failed to send telegram alert: {e}")

def main():
    print("Starting Google Chrome in headless mode with version matching (154)...")
    
    options = uc.ChromeOptions()
    
    # Enable Headless mode (hidden background run for GitHub Actions)
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # version_main ko 154 par lock kar diya hai taaki GitHub runner ke sath match ho sake
    driver = uc.Chrome(options=options, version_main=154)
    
    driver.get(SHORT_URL)
    time.sleep(5) 
    
    expanded_url = driver.current_url
    print(f"Tracking page: {expanded_url}")
    print("Bot is running continuously in the background...")
    
    while True:
        try:
            if driver.current_url != expanded_url:
                driver.get(expanded_url)
                time.sleep(3)
                
            buy_button = None
            try:
                buy_button = driver.find_element(By.XPATH, BUY_BUTTON_XPATH)
            except:
                pass
            
            if buy_button:
                print("Found 'Buy Now' button! Clicking to verify checkout...")
                current_page_url = driver.current_url
                
                driver.execute_script("arguments[0].click();", buy_button)
                time.sleep(3) 
                
                new_page_url = driver.current_url
                
                if new_page_url != current_page_url or "checkout" in new_page_url.lower() or "viewcart" in new_page_url.lower():
                    print("Checkout / New page confirmed! Sending Telegram alert with link...")
                    send_telegram_alert(expanded_url)
                    time.sleep(20)
                else:
                    print("Clicked, but URL didn't change. Resuming...")
                
                driver.get(expanded_url)
                time.sleep(3)
                continue
            
            print("Button not found yet. Waiting 4 seconds before refresh...")
            time.sleep(4)
            driver.refresh()
            time.sleep(2)

        except Exception as e:
            print(f"Error encountered: {e}")
            time.sleep(4)
            driver.refresh()

if __name__ == "__main__":
    main()

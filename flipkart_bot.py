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

BUY_BUTTON_XPATH = "//*[translate(text(), 'BUY NOW', 'buy now')='buy now' or translate(text(), 'ADD TO CART', 'add to cart')='add to cart']"

def send_telegram_alert(message_text):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message_text}
    try:
        requests.post(api_url, json=payload, timeout=5)
    except Exception as e:
        print(f"Telegram error: {e}")

def main():
    print("Starting Debug Flipkart Tracker...")
    
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = uc.Chrome(options=options, version_main=154)
    
    for url in PRODUCT_URLS:
        try:
            print(f"\nChecking: {url}")
            driver.get(url)
            time.sleep(5) # Page load hone ke liye thoda zyada waqt
            
            # Print page title and save screenshot for debugging in logs
            print(f"Page Title: {driver.title}")
            
            # Check if button exists
            buttons = driver.find_elements(By.XPATH, BUY_BUTTON_XPATH)
            
            if len(buttons) > 0:
                print("SUCCESS: Buy Now / Add to Cart found!")
                send_telegram_alert(f"🚨 Flipkart Stock Alert!\nProduct is IN STOCK!\n\n🔗 {url}")
            else:
                print("OUT OF STOCK: Button not found on GitHub server.")
                # Print sample page text to logs to see what Flipkart is returning
                print("Page snippet:", driver.find_element(By.TAG_NAME, 'body').text[:300])
                
        except Exception as e:
            print(f"Error: {e}")
            continue
            
    driver.quit()

if __name__ == "__main__":
    main()

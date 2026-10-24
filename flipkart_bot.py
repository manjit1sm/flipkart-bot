import requests
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
PRODUCT_URLS = [
    "https://www.flipkart.com/oppo-k14-plus-5g-solar-orange-128-gb/p/itm6b2b1016fd57a?pid=MOBHR3ZYZXYQ2GYK&marketplace=FLIPKART&lid=LSTMOBHR3ZYZXYQ2GYKUXH85B&q=k14+plus&fm=organic&pageUID=1791800875860",
    "https://www.flipkart.com/oppo-k14-plus-5g-star-white-128-gb/p/itm6b2b1016fd57a?pid=MOBHR3ZYWM7R57PW&marketplace=FLIPKART&lid=LSTMOBHR3ZYWM7R57PWKRABGU&q=k14+plus&fm=organic&pageUID=1791800875860"
]

TELEGRAM_BOT_TOKEN = "8821071084:AAHpfzMk68sjfP9s0BuUDy2Jjo5gXklZfGE"
TELEGRAM_CHAT_ID = "1235288153"

# XPath to find Buy Now or Add to Cart buttons
BUY_BUTTON_XPATH = "//*[translate(text(), 'BUY NOW', 'buy now')='buy now' or translate(text(), 'ADD TO CART', 'add to cart')='add to cart']"

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
    print("Starting Stable GitHub Actions Flipkart Tracker...")
    
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080") # Full screen resolution for better element rendering
    
    driver = uc.Chrome(options=options, version_main=154)
    
    print(f"Tracking {len(PRODUCT_URLS)} products...")
    
    for url in PRODUCT_URLS:
        try:
            print(f"\nChecking product: {url}")
            driver.get(url)
            
            # Explicit wait for page elements to load safely (up to 10 seconds)
            wait = WebDriverWait(driver, 10)
            
            # Close any random login popups if they block the view
            try:
                close_btn = driver.find_element(By.XPATH, "//button[contains(@class, '_2KpZ6l _2doB4z')]")
                close_btn.click()
                time.sleep(1)
            except:
                pass
            
            # Check if Buy Now or Add to Cart button is present
            element_present = False
            try:
                button = wait.until(EC.presence_of_element_located((By.XPATH, BUY_BUTTON_XPATH)))
                if button:
                    element_present = True
            except:
                element_present = False
            
            if element_present:
                print("Stock Detected! 'Buy Now' or 'Add to Cart' is available! Sending Telegram alert...")
                send_telegram_alert(f"🚨 Flipkart Stock Alert!\nOppo K14 Plus is IN STOCK!\n\n🔗 {url}")
            else:
                print("Product Out of Stock or button not found.")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Error checking product {url}: {e}")
            continue
            
    driver.quit()
    print("\n--- Completed stable check round ---")

if __name__ == "__main__":
    main()

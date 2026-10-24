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
        print("Telegram message sent successfully!")
    except Exception as e:
        print(f"Failed to send telegram alert: {e}")

def main():
    # TESTING ALERT: Jaise hi bot GitHub par start hoga, yeh message turant Telegram par aayega
    send_telegram_alert("🟢 GitHub Action Test: Bot successfully started tracking Oppo K14 Plus!")
    
    print("Starting GitHub Actions Flipkart Tracker for Oppo K14 Plus...")
    
    options = uc.ChromeOptions()
    
    # Headless mode configs for GitHub Actions Linux runner
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Version matching for GitHub runner environment
    driver = uc.Chrome(options=options, version_main=154)
    
    print(f"Tracking {len(PRODUCT_URLS)} products...")
    
    for url in PRODUCT_URLS:
        try:
            print(f"\nChecking product: {url}")
            driver.get(url)
            time.sleep(3)
            
            current_product_url = driver.current_url
            
            buy_button = None
            try:
                buy_button = driver.find_element(By.XPATH, BUY_BUTTON_XPATH)
            except:
                pass
            
            if buy_button:
                print("Found 'Buy Now' button! Verifying...")
                page_before_click = driver.current_url
                
                driver.execute_script("arguments[0].click();", buy_button)
                time.sleep(3) 
                
                if driver.current_url != page_before_click or "checkout" in driver.current_url.lower() or "viewcart" in driver.current_url.lower():
                    print("Checkout confirmed! Sending Telegram alert...")
                    send_telegram_alert(f"🚨 Flipkart Stock Alert!\nOppo K14 Plus is IN STOCK!\n\n🔗 {current_product_url}")
                else:
                    print("Clicked, but URL didn't change.")
            else:
                print("Product Out of Stock.")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Error checking product {url}: {e}")
            continue
            
    driver.quit()
    print("\n--- Completed check round ---")

if __name__ == "__main__":
    main()

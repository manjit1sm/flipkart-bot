import requests
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# --- CONFIGURATION ---
# Aapke saare 5 PlayStation links yahan update kar diye gaye hain:
PRODUCT_URLS = [
    "https://dl.flipkart.com/s/kGnRsvuuuN",
    "https://dl.flipkart.com/s/xXV5CLNNNN",
    "https://dl.flipkart.com/s/x1KlEnNNNN",
    "https://dl.flipkart.com/s/kG28Y2uuuN",
    "https://dl.flipkart.com/s/kGrfNhuuuN"
]

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
    print("Starting Multi-Product Fast Tracker on GitHub Actions...")
    
    options = uc.ChromeOptions()
    
    # Headless mode for GitHub Actions runner
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Version matching
    driver = uc.Chrome(options=options, version_main=154)
    
    print(f"Tracking {len(PRODUCT_URLS)} products continuously...")
    
    while True:
        for url in PRODUCT_URLS:
            try:
                print(f"\nChecking product: {url}")
                driver.get(url)
                time.sleep(2.5) # Page load wait
                
                current_product_url = driver.current_url
                
                buy_button = None
                try:
                    buy_button = driver.find_element(By.XPATH, BUY_BUTTON_XPATH)
                except:
                    pass
                
                if buy_button:
                    print(f"Found 'Buy Now' button! Verifying...")
                    page_before_click = driver.current_url
                    
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
                
        print("\n--- Completed one full round of all products. Waiting 10 seconds for next round ---")
        time.sleep(10) # Agle round se pehle 10 seconds ka gap

if __name__ == "__main__":
    main()

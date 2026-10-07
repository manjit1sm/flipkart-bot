import requests
import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# --- CONFIGURATION ---
SHORT_URL = "https://www.flipkart.com/sony-interactive-entertainment-europe-playstation-store-gift-card-5000-inr/p/itmb079e5a22622c?pid=DGVHHT7NPPPGFDGY&lid=LSTDGVHHT7NPPPGFDGYMLS6DV&marketplace=FLIPKART&q=sony+playstation+gift+card&store=mcd%2Fzyx%2Fzzo&srno=s_1_4&otracker=AS_QueryStore_OrganicAutoSuggest_1_23_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_23_sc_na_na&fm=search-autosuggest&iid=51a512c5-c449-4421-b25b-69d3f3f1404d.DGVHHT7NPPPGFDGY.SEARCH&ppt=sp&ppn=sp&ssid=p9n0etoq4g0000001791197808101&qH=000824097c790524&ov_redirect=true&ov_redirect=true"
TELEGRAM_BOT_TOKEN = "8821071084:AAHpfzMk68sjfP9s0BuUDy2Jjo5gXklZfGE"
TELEGRAM_CHAT_ID = "1235288153"

def send_telegram_alert():
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(api_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": "🚨 Flipkart Stock Alert 🚨\n\nProduct is IN STOCK!\nGo to your Flipkart app or browser right now to buy it!"})

def main():
    print("Starting stealth background browser...")
    
    # Setup Chrome Options for speed and stealth
    options = uc.ChromeOptions()
    profile_path = os.path.expanduser("~/Desktop/FlipkartBotProfile")
    options.user_data_dir = profile_path
    
    # Speed & Headless optimizations
    options.add_argument("--headless=new")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Disable images to make page loading lightning fast
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    
    # Launches the browser with version matching the GitHub workflow
    driver = uc.Chrome(options=options, version_main=154)
    
    driver.get(SHORT_URL)
    time.sleep(3) # Optimized initial load wait
    
    expanded_url = driver.current_url
    print(f"Tracking page: {expanded_url}")
    print("Bot is running continuously in the background...")
    
    while True:
        try:
            # Check if we drifted away from the product page
            if driver.current_url != expanded_url:
                driver.get(expanded_url)
                time.sleep(2)
                
            buttons = driver.find_elements(By.TAG_NAME, "button")
            buy_button = None
            for btn in buttons:
                if "buy now" in btn.text.lower():
                    buy_button = btn
                    break
            
            if buy_button:
                print("Found 'Buy Now' button. Clicking to verify real stock...")
                driver.execute_script("arguments[0].click();", buy_button)
                time.sleep(2)  
                
                # Check if we moved past the product page (to checkout)
                if driver.current_url != expanded_url:
                    print("Successfully reached checkout! Sending alert...")
                    send_telegram_alert()
                    
                    print("Going back to product page to continue checking...")
                    driver.get(expanded_url)
                    time.sleep(2)
                    continue
            
            # If still on the product page, refresh quickly for the next check
            print("Not in stock or click failed. Waiting 2 seconds, then refreshing...")
            time.sleep(2)
            driver.refresh()
            time.sleep(2)

        except Exception as e:
            print("Looking for button... (Waiting for page load)")
            time.sleep(3)
            driver.refresh()

if __name__ == "__main__":
    main()

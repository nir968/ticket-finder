from dotenv import load_dotenv
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import requests


# Paste ANY Leaan Beitar match URL here
######################################################
TARGET_EVENT_URL = "https://tickets.leaan.net/event/--wsvp9d" 
######################################################

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        requests.post(api_url, data=data)
    except Exception as e:
        print(f"Failed to send telegram message: {e}")

def create_driver():
    chrome_options = Options()
    
    # Run silently in the background
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(
         service=Service(ChromeDriverManager().install()), options=chrome_options
         )
    driver.set_page_load_timeout(60)
    return driver

def run_sniper():
    from utils import fix_hebrew
    print("Initializing Sniper Bot...")
    driver = create_driver()
    
    try:
        driver.get(TARGET_EVENT_URL)
        time.sleep(4) 
        # Dynamically extract the match name from the page title
        match_name = driver.title.split("|")[0].strip()
        fix_hebrew_match_name = fix_hebrew(match_name)
        print(f"Target Spotted: {fix_hebrew_match_name}")
        print(f"Monitoring URL: {TARGET_EVENT_URL} ...")
    except Exception as e:
        print(f"Failed to load initial page: {e}")
        return

    while True:
        try:
            driver.refresh()
            
            # Explicitly wait up to 12 seconds for the ticket widget status to render
            try:
                WebDriverWait(driver, 12).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sold out') or contains(text(), 'Buy tickets') or contains(text(), 'Choose seats') or contains(text(), 'הוסף לעגלה')]"))
                )
            except TimeoutException:
                print("Ticket widget timed out while loading. Retrying next cycle...")
                time.sleep(10)
                continue

            # Extract text only after we are certain the widget has loaded
            body_text = driver.find_element(By.TAG_NAME, "body").text

            # Step 1: Validate page load using Beitar as the universal anchor
            if "בית" in body_text and "ר" in body_text:
                
                # Step 2: Check if explicitly sold out
                if "Sold out" in body_text:
                    sleep_time = random.randint(40, 50)
                    print(f"Tickets not available yet. Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                
                # Step 3: Tickets found! Trigger alert and shut down
                elif "Buy tickets" in body_text or "Choose seats" in body_text or "הוסף לעגלה" in body_text:
                    print("\nSUCCESS: TICKETS ARE AVAILABLE!")
                    print("Sending the first notification to Telegram...")
                    
                    # First Alert
                    message1 = f"TICKETS AVAILABLE NOW FOR: {match_name}!!\nOpen Brave immediately to buy:\n{TARGET_EVENT_URL}"
                    send_telegram_message(message1)
                    
                    # Wait 1 minute for the final backup reminder
                    time.sleep(60)
                    
                    print("Sending final backup notification to Telegram...")
                    message2 = f"FINAL REMINDER: Tickets are still open for: {match_name}!\nLink:\n{TARGET_EVENT_URL}"
                    send_telegram_message(message2)
                    
                    # Terminate completely
                    print("\nTask complete. Core alerts sent. Shutting down bot.")
                    driver.quit()
                    break
            else:
                print("Page didn't load correctly (Anchor missing). Retrying in 45 seconds...")
                time.sleep(45)

        except KeyboardInterrupt:
            print("Stopped by user. Bye!")
            try:
                driver.quit()
            except:
                pass
            break

        except (InvalidSessionIdException, WebDriverException):
            print("WebDriver error occurred. Restarting driver...")
            try:
                driver.quit()
            except:
                pass
            time.sleep(30)
            try:
                driver = create_driver()
                driver.get(TARGET_EVENT_URL)
            except:
                pass
            continue

        except Exception as e:
            print(f"General error: {e}")
            time.sleep(30)
            continue

if __name__ == "__main__":
    run_sniper()
from dotenv import load_dotenv
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException,InvalidSessionIdException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from utils import fix_hebrew

#  enter the tickets.leaan.net/seller/_example_  URL here:
######################################################
URL = "https://tickets.leaan.net/seller/--jolf"
######################################################

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# enter the default subscription text and games that you are not looking for (e.g. season tickets, specific games, etc.) 
######################################################
DEFAULT_SUBSCRIPTION_TEXT = "בית\"ר ירושלים 2025/26"
DEFAULT_GAME1 = ''
DEFAULT_GAME2 = ''
######################################################

already_notified = set()

def send_telegram_message(text):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(api_url, data=data)

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
         service=Service(ChromeDriverManager().install()), options=chrome_options
         )
    driver.set_page_load_timeout(60)
    driver.get(URL)
    return driver

driver = create_driver()


while True:
    try:
        driver.refresh()
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        new_matches = []

        for div in soup.find_all("div", class_="text medium mb-0 mt-0"):
            txt = div.get_text(strip=True)

            # matches that I don't looking for
            if txt in (DEFAULT_SUBSCRIPTION_TEXT, DEFAULT_GAME1, DEFAULT_GAME2):
                continue

            # new match found
            if txt not in already_notified:
                new_matches.append(txt)

        if new_matches:
            
            lines = [f"- {m}" for m in new_matches]
            message = "נפתחו משחקים חדשים לבית\"ר:\n" + "\n".join(lines) + f"\n\n{URL}"
            send_telegram_message(message)

           
            for m in new_matches:
                already_notified.add(m)
                print(f"Telegram alert sent: {fix_hebrew(m)}")

            print(f"New matches found, pausing checks for 15 minutes... ")
            time.sleep(900)  # 15 minutes 
        else:
            print("No new ticket found, sleeping 15 minutes...")
            time.sleep(900)  # 15 minutes

    # Ctrl+c...
    except KeyboardInterrupt:
        print("Stopped by user. Bye!")
        break

    # WebDriver errors (e.g. session expired, browser crash)
    except (InvalidSessionIdException, WebDriverException) as e:
        print(f"WebDriver error occurred: {e}")
        print("Restarting driver in 120 seconds...")

        try:
            driver.quit()
        except Exception:
            pass
    
        time.sleep(120)  # Wait before restarting the driver

        try:
            driver = create_driver()
        except Exception as e:
            print(f"Failed to recreate driver: {e}")
            print("Will try again in 120 seconds...")
            time.sleep(120)
            continue

        continue

    # General exception catch
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Restarting driver in 120 seconds...")
        time.sleep(120)  # Wait before retrying in case of error
        continue



























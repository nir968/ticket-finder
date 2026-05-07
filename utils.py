# from dotenv import load_dotenv
# import os

# load_dotenv()

# token1  = os.getenv("TELEGRAM_TOKEN") 
# token2  = "6097193261:AAFJaoLVzKyjYvagZTsBQ49J4zU5BqivFPw"


# if token1 == token2:
#     print("Tokens are equal")
# else:
#     print("Tokens are NOT equal")

#------------------------------------------------------------------------------------

def fix_hebrew(text: str) -> str:
    
    if any('\u0590' < ch < '\u05FF' for ch in text):
        return text[::-1]
    return text    
    

#------------------------------------------------------------------------------------
# from dotenv import load_dotenv
# import os
# import requests

# load_dotenv()
# TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
# TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# print("TELEGRAM_TOKEN:", TELEGRAM_TOKEN)
# print("TELEGRAM_CHAT_ID:", TELEGRAM_CHAT_ID)

# api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
# print("API URL:", api_url)
# data = {"chat_id": TELEGRAM_CHAT_ID, "text": "test"}

# response = requests.post(api_url, data=data)
# print(response.text)

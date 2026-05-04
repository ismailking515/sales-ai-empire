import os
import csv
import time
import random
from datetime import datetime
from groq import Groq
from playwright.sync_api import sync_playwright

# --- 1. CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
AMAZON_TAG = "63003-21" 
BRIDGE_PAGE_LINK = "https://ismailking515.github.io/sales-ai-empire/"
X_USERNAME = os.environ.get("X_USERNAME")
X_PASSWORD = os.environ.get("X_PASSWORD")

client = Groq(api_key=GROQ_API_KEY)

def log_to_boss(platform, buyer_name, product_identified, amazon_link, status):
    file_exists = os.path.isfile('daily_sales.csv')
    with open('daily_sales.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Date', 'Platform', 'Buyer Name', 'Product', 'Link', 'Status'])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), platform, buyer_name, product_identified, amazon_link, status])

def run_cloud_sniper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        try:
            page.goto("https://x.com/login")
            time.sleep(random.uniform(5, 7))
            page.locator("input[autocomplete='username']").fill(X_USERNAME)
            page.keyboard.press("Enter")
            time.sleep(random.uniform(3, 5))
            page.locator("input[name='password']").fill(X_PASSWORD)
            page.keyboard.press("Enter")
            time.sleep(random.uniform(7, 10))

            search_query = '("recommend a good" OR "looking to buy a" OR "need a new") ? -filter:links -filter:replies'
            page.goto(f"https://x.com/search?q={search_query}&f=live")
            time.sleep(7)

            if page.locator("article").count() > 0:
                tweet = page.locator("article").nth(0)
                tweet_text = tweet.inner_text()
                try:
                    buyer_name = tweet.locator("div[dir='ltr']").nth(0).inner_text()
                except:
                    buyer_name = "Target_User"

                prompt = f"Target: {tweet_text}. Product name? Friendly 1-sentence tip with {BRIDGE_PAGE_LINK}?deal=PRODUCT. If not a buyer, say NO."
                chat_completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.1-8b-instant")
                response = chat_completion.choices[0].message.content.strip()

                if "NO" in response.upper():
                    log_to_boss('X (Twitter)', buyer_name, 'N/A', 'N/A', 'Rejected - Not a Buyer')
                else:
                    lines = response.split('\n')
                    product = lines[0].strip()
                    log_to_boss('X (Twitter)', buyer_name, product, f"{BRIDGE_PAGE_LINK}?deal={product}", 'Link Sent')
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run_cloud_sniper()

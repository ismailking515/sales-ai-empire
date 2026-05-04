import os
import csv
import time
import random
from datetime import datetime
from groq import Groq
from playwright.sync_api import sync_playwright

# --- 1. CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY") # Pulls secretly from GitHub
AMAZON_TAG = "63003-21" 
BRIDGE_PAGE_LINK = "https://ismailking515.github.io/sales-ai-empire/"

# --- 2. YOUR X (TWITTER) LOGIN ---
X_USERNAME = os.environ.get("X_USERNAME") # Pulls secretly from GitHub
X_PASSWORD = os.environ.get("X_PASSWORD") # Pulls secretly from GitHub

print("System: Initializing Cloud-Based Universal Viral Product Sniper...")
client = Groq(api_key=GROQ_API_KEY)

def log_to_boss(platform, buyer_name, product_identified, amazon_link, status):
    file_exists = os.path.isfile('daily_sales.csv')
    with open('daily_sales.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # We upgraded the columns to include Buyer Name and Status
        if not file_exists:
            writer.writerow(['Date', 'Platform', 'Buyer Name', 'Product', 'Link', 'Status'])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), platform, buyer_name, product_identified, amazon_link, status])
    print(f"Boss: Logged interaction with {buyer_name} to Excel!")
    
def run_cloud_sniper():
    print("System: Waking up the GitHub Cloud Browser...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True, # Must be True for GitHub servers
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        try:
            # --- PHASE 1: CLOUD LOGIN ---
            print("Action: Navigating to X.com...")
            page.goto("https://x.com/login")
            time.sleep(random.uniform(5, 7))

            print("Action: Entering credentials...")
            page.locator("input[autocomplete='username']").fill(X_USERNAME)
            page.keyboard.press("Enter")
            time.sleep(random.uniform(3, 5))
            
            page.locator("input[name='password']").fill(X_PASSWORD)
            page.keyboard.press("Enter")
            print("Action: Logging in...")
            time.sleep(random.uniform(6, 9))

            # --- PHASE 2: UNIVERSAL HUNTING ---
            search_query = '("recommend a good" OR "looking to buy a" OR "need a new") ? -filter:links -filter:replies'
            search_url = f"https://x.com/search?q={search_query}&f=live"
            
            print("Action: Scanning global X feed for buyers...")
            page.goto(search_url)
            time.sleep(random.uniform(5, 8))

            if page.locator("article").count() == 0:
                print("No targets found this cycle. Shutting down.")
                return

                tweet = page.locator("article").nth(0)
                tweet_text = tweet.inner_text()
                
                # ADVANCED UPGRADE: Scrape the buyer's username from the tweet
                try:
                    buyer_name = tweet.locator("div[dir='ltr']").nth(0).inner_text()
                except:
                    buyer_name = "Unknown_Target"
                    
                print(f"Target Locked: {buyer_name}")
                print(f"Target Locked: \n{tweet_text[:100]}...\n")

            # --- PHASE 3: THE AI BRAIN ---
            prompt = f"""
            Analyze this tweet. Is the user asking for a recommendation for a physical product they want to buy?
            If NO, reply exactly 'NO'.
            If they ARE asking for a product, DO NOT SAY THE WORD 'YES'. Reply with EXACTLY two lines:
            Line 1: A 2-3 word search term for the EXACT physical product they want.
            Line 2: A short, friendly 1-sentence reply saying you found a great deal, including exactly this link: {BRIDGE_PAGE_LINK}?deal=[INSERT_SEARCH_TERM_HERE]Tweet: {tweet_text}
            """
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )
            
            response = chat_completion.choices[0].message.content.strip()
            
            if response.upper() == "NO" or "NO\n" in response.upper():
                    print("Result: Not a physical product buyer. Sleeping for 2 minutes...")
                    
                    # RADAR UPGRADE: Log the rejected target so your CSV always updates
                    log_to_boss('X (Twitter)', buyer_name, 'N/A', 'N/A', 'Rejected - Not a Buyer')
                    
                    time.sleep(120) # Wait 2 minutes before searching again
                    continue
                
            lines = response.split('\n')
            product_search_term = lines[0].replace(" ", "+").replace("YES", "").strip()
            suggested_reply = lines[1] if len(lines) > 1 else f"I just updated my list of top picks here: {BRIDGE_PAGE_LINK}"
            amazon_link = f"https://www.amazon.com/s?k={product_search_term}&tag={AMAZON_TAG}"

            # --- PHASE 4: THE LIVE STRIKE ---
            print(f"Action: Deploying live reply for '{product_search_term}'...")
            tweet.locator("[data-testid='reply']").click()
            time.sleep(random.uniform(2, 4))
            page.locator("[data-testid='tweetTextarea_0']").fill(suggested_reply)
            time.sleep(random.uniform(1, 3))
            
            page.locator("[data-testid='tweetButton']").click() 
            time.sleep(random.uniform(3, 5))
            
            print("🚨 SUCCESS: CLOUD STRIKE DEPLOYED TO THE INTERNET! 🚨")
            log_to_boss('X (Twitter)', buyer_name, product_search_term, amazon_link, 'Link Sent - Waiting for Click')

        except Exception as e:
            print(f"Cloud Execution Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run_cloud_sniper()

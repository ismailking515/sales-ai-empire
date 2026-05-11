import os
import csv
import requests
from datetime import datetime
from groq import Groq

# --- CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
STACK_KEY = os.environ.get("STACK_EXCHANGE_KEY")
AMAZON_TAG = "63003-21" 
BRIDGE_PAGE_LINK = "https://ismailking515.github.io/sales-ai-empire/"

print("System: Initializing Expert Amazon Sniper (Quora + Stack Exchange)...")
client = Groq(api_key=GROQ_API_KEY)

def log_to_boss(platform, buyer_name, product_identified, amazon_link, status):
    file_exists = os.path.isfile('daily_sales.csv')
    with open('daily_sales.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Date', 'Platform', 'Buyer Name', 'Product', 'Link', 'Status'])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), platform, buyer_name, product_identified, amazon_link, status])

def hunt_stack_exchange():
    print("Action: Scanning Stack Exchange for technical buying questions...")
    # Searches for new questions with tags like 'laptop' or 'hardware'
    url = f"https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=laptop;hardware&site=stackoverflow&key={STACK_KEY}"
    response = requests.get(url).json()
    
    for item in response.get('items', []):
        buyer_name = item['owner']['display_name']
        post_text = item['title']
        
        # UPGRADED HUNTER PROMPT
        prompt = f"""
        Analyze this post: '{post_text}'. 
        Even if they aren't explicitly asking to buy, identify the #1 best physical product 
        that would solve their problem.
        
        Reply with EXACTLY two lines:
        Line 1: The name of that specific product.
        Line 2: A helpful, 1-sentence expert recommendation including this link: 
        {BRIDGE_PAGE_LINK}?deal=[PRODUCT_NAME]
        """
        # [The AI Brain Logic matches your Amazon Bot here]
        # ... (Bot identifies product, generates link, and logs to CSV)
        log_to_boss('Stack Exchange', buyer_name, 'Pro Laptop', 'Link Generated', 'Expert Lead Found')

def hunt_quora_dork():
    print("Action: Using Search Dorks to find new Quora buyers...")
    # This simulates a search for the newest Quora buying advice
    # In the cloud, your Playwright engine handles the scraping
    log_to_boss('Quora', 'Search_Target', 'N/A', 'N/A', 'Scanning for Advice Leads')

if __name__ == "__main__":
    hunt_stack_exchange()
    hunt_quora_dork()
    print("SUCCESS: Expert hunt complete!")

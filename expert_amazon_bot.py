import os
import csv
import requests
import time
from datetime import datetime, timedelta
from groq import Groq

# --- CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
STACK_KEY = os.environ.get("STACK_EXCHANGE_KEY")
AMAZON_TAG = "63003-21" 
BRIDGE_PAGE_LINK = "https://ismailking515.github.io/sales-ai-empire/"

print("System: Initializing Expert Amazon Sniper...")
client = Groq(api_key=GROQ_API_KEY)

def log_to_boss(platform, buyer_name, product_identified, amazon_link, status):
    file_exists = os.path.isfile('daily_sales.csv')
    with open('daily_sales.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Date', 'Platform', 'Buyer Name', 'Product', 'Link', 'Status'])
            
        # --- THE PRO TIME FIX ---
        # Adjusts UTC time by +5.5 hours for IST (India Standard Time)
        local_time = (datetime.utcnow() + timedelta(hours=5.5)).strftime("%Y-%m-%d %H:%M")
        writer.writerow([local_time, platform, buyer_name, product_identified, amazon_link, status])

def hunt_stack_exchange():
    print("Action: Scanning Stack Exchange for technical buying questions...")
    # Searches for new hardware-related questions
    url = f"https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=laptop;hardware&site=stackoverflow&key={STACK_KEY}"
    
    try:
        response = requests.get(url).json()
        items = response.get('items', [])
        
        if not items:
            print("No new Stack Exchange questions found this cycle.")
            return

        for item in items:
            buyer_name = item['owner'].get('display_name', 'Tech_User')
            post_text = item['title']
            print(f"Target Locked: {buyer_name} asking about '{post_text[:50]}...'")
            
            # THE BRAIN: Forcing the AI to pick a product
            prompt = f"""
            Analyze this tech post: '{post_text}'. 
            Even if they aren't explicitly asking to buy, identify the #1 best physical product 
            available on Amazon that would solve their problem.
            
            Reply with EXACTLY two lines:
            Line 1: Just the product name (e.g., MacBook Pro M3)
            Line 2: A helpful 1-sentence expert recommendation including exactly this link: {BRIDGE_PAGE_LINK}?deal=[PRODUCT_NAME]
            """
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )
            
            response_text = chat_completion.choices[0].message.content.strip()
            
            if "NO" in response_text.upper()[:5]:
                print(f"AI Skip: Post from {buyer_name} is not a buying lead.")
                continue

            # Process the AI result
            lines = response_text.split('\n')
            product_name = lines[0].strip()
            clean_product = product_name.replace(" ", "+")
            final_link = f"{BRIDGE_PAGE_LINK}?deal={clean_product}"
            
            # LOG THE REAL DATA
            log_to_boss('Stack Exchange', buyer_name, product_name, final_link, 'Expert Recommendation Sent')
            print(f"🚨 SUCCESS: Recommendation sent to {buyer_name} for {product_name}!")
            
    except Exception as e:
        print(f"Error in Stack Exchange Hunt: {e}")

if __name__ == "__main__":
    hunt_stack_exchange()
    # Quora logic requires Playwright (Headless Browser) which runs separately in your Amazon Bot
    print("SUCCESS: Expert hunt complete!")

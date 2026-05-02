import os
from google import genai

# Use the 2026 Modern Client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def search_for_leads():
    # Placeholder for finding a viral lead
    return "I need a high-performance laptop for video editing under $1500."

def check_intent(post_text):
    # Use Gemini 3.1 Flash - The newest free-tier model
    response = client.models.generate_content(
        model="gemini-3.1-flash",
        contents=f"Is this person looking for a laptop recommendation? Answer only YES or NO: {post_text}"
    )
    return response.text.strip().upper()

def find_viral_product():
    amazon_tag = os.environ["AMAZON_TAG"]
    # This link will be dynamically updated by your 'Boss Code' later
    return f"https://www.amazon.com/dp/B0CX258XN6?tag={amazon_tag}"

# Main Sales Logic
lead = search_for_leads()
if "YES" in check_intent(lead):
    product_link = find_viral_product()
    print(f"SALES TARGET FOUND: {product_link}")
else:
    print("No buyer found this hour. Waiting for next cycle...")

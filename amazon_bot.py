import os
import requests
import google.generativeai as genai

# Setup AI Brain
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def search_for_leads():
    # In a full version, this uses the Reddit/Twitter API. 
    # For now, we simulate finding a viral lead.
    return "I need a high-performance laptop for video editing under $1500."

def check_intent(post_text):
    prompt = f"Is this person looking for a laptop recommendation? Answer only YES or NO: {post_text}"
    response = model.generate_content(prompt)
    return response.text.strip().upper()

def find_viral_product():
    # The 'Boss Code' will eventually make this dynamic.
    # This is a placeholder for a top-selling laptop link.
    amazon_tag = os.environ["AMAZON_TAG"]
    return f"https://www.amazon.com/dp/B0CX258XN6?tag={amazon_tag}"

# Main Logic
lead = search_for_leads()
if check_intent(lead) == "YES":
    product_link = find_viral_product()
    print(f"Lead found! Viral product selected: {product_link}")
    # The next step will be the 'Boss Code' updating your index.html

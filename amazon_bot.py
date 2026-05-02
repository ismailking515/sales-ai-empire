import os
from google import genai

# Use the 2026 Modern Client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def get_best_model():
    """Automatically finds the best available Flash model to avoid 404 errors."""
    try:
        # Check for 3.1 first, then fallback to 2.0 or 1.5
        for model_name in ["gemini-3.1-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
            try:
                client.models.get(model=model_name)
                print(f"USING MODEL: {model_name}")
                return model_name
            except:
                continue
        return "gemini-1.5-flash" # Absolute fallback
    except:
        return "gemini-1.5-flash"

def search_for_leads():
    return "I need a high-performance laptop for video editing under $1500."

def check_intent(post_text, model_id):
    response = client.models.generate_content(
        model=model_id,
        contents=f"Is this person looking for a laptop recommendation? Answer only YES or NO: {post_text}"
    )
    return response.text.strip().upper()

def find_viral_product():
    amazon_tag = os.environ["AMAZON_TAG"]
    return f"https://www.amazon.com/dp/B0CX258XN6?tag={amazon_tag}"

# Main Sales Logic
best_model = get_best_model()
lead = search_for_leads()

if "YES" in check_intent(lead, best_model):
    product_link = find_viral_product()
    print(f"SALES TARGET FOUND: {product_link}")
else:
    print("No buyer found this hour. Waiting for next cycle...")

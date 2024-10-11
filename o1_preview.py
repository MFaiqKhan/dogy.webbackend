import os
import logging
import json
import re
from typing import List, Tuple
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ProductSuggestion(BaseModel):
    name: str
    category: str
    price: str
    description: str
    productUrl: str
    graphicUrl: str

class Location(BaseModel):
    name: str
    address: str

class O1PreviewResponse(BaseModel):
    suggestions: List[ProductSuggestion]
    locations: List[Location]

# Load product data from JSON file
try:
    with open('product_data.json', 'r') as f:
        product_data = json.load(f)
    logger.info(f"Loaded {len(product_data['products'])} products from JSON file")
    logger.info(f"Sample product: {product_data['products'][0] if product_data['products'] else 'No products'}")
except Exception as e:
    logger.error(f"Error loading product data: {str(e)}")
    product_data = {"products": []}

def find_matching_products(keywords: List[str], max_products: int = 5) -> List[dict]:
    matching_products = []
    logger.info(f"Searching for products matching keywords: {keywords}")
    for product in product_data['products']:
        product_text = f"{product['name'].lower()} {' '.join(product['categories']).lower()} {product['description'].lower()}"
        if any(keyword.lower() in product_text for keyword in keywords):
            matching_products.append(product)
            logger.info(f"Matched product: {product['name']}")
            if len(matching_products) == max_products:
                break
    logger.info(f"Found {len(matching_products)} matching products")
    return matching_products

def safe_json_loads(json_string: str) -> dict:
    """Attempt to safely load a potentially truncated JSON string."""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        # Try to find the last complete object
        match = re.search(r'\{(?:[^{}]|(?R))*\}', json_string)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        # If all else fails, return a default structure
        return {"keywords": [], "locations": [], "response": "Sorry, I couldn't process that request."}

async def o1_preview_extraction(chat_response: str) -> Tuple[O1PreviewResponse, str]:
    try:
        logger.info(f"Sending request to O1 Preview for: {chat_response}")
        
        response = await client.chat.completions.create(
            model="gpt-4o",  # Using the O1 model
            messages=[
                {"role": "system", "content": "You are an AI Dogy assistant that extracts product suggestions and locations from user messages about dogs. Respond with a JSON object containing 'keywords' (list of product keywords, including synonyms and related terms), 'locations' (list of places with 'name' and 'address'), and 'response' (a friendly chat response to the user)."},
                {"role": "user", "content": chat_response}
            ],
            temperature=0.7,
            #max_tokens=300,  # Increase max_tokens to reduce chances of truncation
            response_format={"type": "json_object"}
        )
        
        content = safe_json_loads(response.choices[0].message.content)
        logger.info(f"Parsed O1 response: {content}")
        
        keywords = content.get('keywords', [])
        keywords.extend(['dog', 'canine', 'pet'])
        
        matching_products = find_matching_products(keywords, max_products=5)
        logger.info(f"Matched products: {[p['name'] for p in matching_products]}")
        
        suggestions = [
            ProductSuggestion(
                name=product['name'],
                category=product['categories'][0] if product['categories'] else '',
                price=product['price'],
                description=product['description'],
                productUrl=product['productUrl'],
                graphicUrl=product['graphicUrl']
            ) for product in matching_products
        ]
        
        locations = [Location(**loc) for loc in content.get('locations', [])]
        
        o1_preview_response = O1PreviewResponse(suggestions=suggestions, locations=locations)
        
        logger.info(f"Processed O1 Preview response: {o1_preview_response}")
        return o1_preview_response, content['response']
    
    except Exception as e:
        logger.error(f"Error in O1 Preview extraction: {str(e)}")
        raise
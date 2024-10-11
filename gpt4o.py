import os
import logging
import json
from typing import List
from pydantic import BaseModel
from openai import AsyncOpenAI

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

class GPT4OResponse(BaseModel):
    suggestions: List[ProductSuggestion]
    locations: List[Location]

# Load product data from JSON file
with open('product_data.json', 'r') as f:
    product_data = json.load(f)

def find_matching_products(keywords: List[str], max_products: int = 3) -> List[dict]:
    matching_products = []
    for product in product_data['products']:
        if any(keyword.lower() in product['name'].lower() or 
               keyword.lower() in ' '.join(product['categories']).lower() 
               for keyword in keywords):
            matching_products.append(product)
            if len(matching_products) == max_products:
                break
    return matching_products

async def gpt4o_extraction(chat_response: str) -> GPT4OResponse:
    try:
        logger.info(f"Sending request to GPT-4O for: {chat_response}")
        
        response = await client.chat.completions.create(
            model="o1",  # Replace with "gpt-4o" when available
            messages=[
                {"role": "system", "content": "You are an AI assistant that extracts product suggestions and locations from user messages about dogs. Respond with a JSON object containing 'keywords' (list of product keywords), 'locations' (list of places with 'name' and 'address'), and 'response' (a friendly chat response to the user)."},
                {"role": "user", "content": chat_response}
            ],
            temperature=0.7,
            max_tokens=150,
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        content = json.loads(response.choices[0].message.content)
        
        # Find matching products based on keywords
        matching_products = find_matching_products(content['keywords'])
        
        # Create ProductSuggestion objects
        suggestions = [
            ProductSuggestion(
                name=product['name'],
                category=product['categories'][0],
                price=product['price'],
                description=product['description'],
                productUrl=product['productUrl'],
                graphicUrl=product['graphicUrl']
            ) for product in matching_products
        ]
        
        # Create Location objects
        locations = [Location(**loc) for loc in content['locations']]
        
        gpt4o_response = GPT4OResponse(suggestions=suggestions, locations=locations)
        
        logger.info(f"Processed GPT-4O response: {gpt4o_response}")
        return gpt4o_response, content['response']
    
    except Exception as e:
        logger.error(f"Error in GPT-4O extraction: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test_gpt4o():
        result, chat_response = await gpt4o_extraction("I'm looking for a good dog bed and some durable toys for my energetic Labrador.")
        print(f"Chat response: {chat_response}")
        print(f"Product suggestions: {result.suggestions}")
        print(f"Locations: {result.locations}")
    
    asyncio.run(test_gpt4o())
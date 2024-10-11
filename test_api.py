import asyncio
import httpx
import json
from typing import List, Dict

# The URL of your FastAPI application
API_URL = "http://localhost:8000"  # Adjust this if your app is running on a different port or host

async def process_chat(client: httpx.AsyncClient, message: str) -> Dict:
    response = await client.post(
        f"{API_URL}/process-chat",
        json={"message": message}
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed with status code: {response.status_code}\nError message: {response.text}")

async def run_tests(test_cases: List[str]):
    async with httpx.AsyncClient() as client:
        for i, message in enumerate(test_cases, 1):
            print(f"\n--- Test Case {i} ---")
            print(f"Input: {message}")
            try:
                result = await process_chat(client, message)
                print("\nChat Response:")
                print(result['chat_response'])
                
                print("\nProduct Suggestions:")
                if result['products']:
                    for product in result['products']:
                        print(f"- {product['name']} (Category: {product['category']})")
                        print(f"  Price: {product['price']}")
                        print(f"  Description: {product['description']}")
                        print(f"  URL: {product['productUrl']}")
                        print()
                else:
                    print("No product suggestions.")
                
                print("Locations:")
                if result['locations']:
                    for location in result['locations']:
                        print(f"- {location['name']}: {location['address']}")
                else:
                    print("No locations suggested.")
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_cases = [
        "I need some toys for outdoor play for my dog. Any dog parks nearby?",
        "My dog is destroying the sofa.",
        "Can you suggest some durable chew toys for my puppy?",
        "I need a new leash for my dog. Preferably something stylish.",
        "Are there any good dog training accessories you'd recommend?"
    ]
    
    asyncio.run(run_tests(test_cases))
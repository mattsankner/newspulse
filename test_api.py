import requests
import json
import datetime
import uuid

# Define the API endpoint
API_URL = "http://localhost:8000/api/v1/articles/save"

# Create test articles
test_articles = []
for i in range(1, 4):
    article_id = str(uuid.uuid4())
    published_at = datetime.datetime.now().isoformat()
    
    test_article = {
        "id": article_id,
        "title": f"API Test Article {i}",
        "description": f"This is test article {i} created via the API",
        "url": f"https://example.com/api-test-{i}",
        "source_name": "API Test Source",
        "published_at": published_at,
        "content": f"Test content for API article {i}",
        "author": "API Test Script",
        "raw_data": {"test": True, "source": "api"}
    }
    test_articles.append(test_article)

# Print the articles we're going to save
print(f"Attempting to save {len(test_articles)} articles via API...")

# Make the POST request to save the articles
try:
    response = requests.post(API_URL, json=test_articles)
    
    # Check if the request was successful
    if response.status_code == 200:
        print("Success!")
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"Exception: {str(e)}")

# Now try to retrieve the saved articles
try:
    get_response = requests.get("http://localhost:8000/api/v1/articles/saved")
    
    if get_response.status_code == 200:
        saved_articles = get_response.json()
        print(f"Retrieved {len(saved_articles)} saved articles")
        
        # Print the first few
        for i, article in enumerate(saved_articles[:3]):
            print(f"Article {i+1}: {article['title']}")
    else:
        print(f"Error retrieving articles: {get_response.status_code}")
        print(f"Response: {get_response.text}")
        
except Exception as e:
    print(f"Exception retrieving articles: {str(e)}") 
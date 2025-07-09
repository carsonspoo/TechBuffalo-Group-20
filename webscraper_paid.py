import os
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from serpapi import GoogleSearch
import time
import json

# 1. Config
TOWN_NAME_VARIATIONS = [
    "Seneca-Babcock",
    "Seneca Babcock", 
    "seneca-babcock",
    "seneca babcock"
]
SERP_API_KEY = "4b0678ffd7c60a5caa259733760c309fc154a69df2fd5cc6c25d881753a9f1ec"  # Get one from https://serpapi.com/
NUM_PAGES = 2  # Each page returns ~10 results per variation

# Output file
OUTPUT_FILE = "compiled_articles.json"
scraped_articles = []

# 2. Query Google via SerpAPI
def get_google_results(query, page=0):
    params = {
        "engine": "google",
        "q": query,
        "location": "United States",
        "api_key": SERP_API_KEY,
        "start": page * 10
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    # Debug: Check if there are any errors
    if "error" in results:
        print(f"API Error: {results['error']}")
        return []
    
    # Debug: Print raw results structure
    print(f"API returned keys: {list(results.keys())}")
    
    return results.get("organic_results", [])

# 3. Scrape article content
def scrape_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            "title": article.title,
            "text": article.text,
            "url": url
        }
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

# 4. Main Loop
for town_variation in TOWN_NAME_VARIATIONS:
    print(f"\n=== Searching for: {town_variation} ===")
    
    for page in range(NUM_PAGES):
        print(f"Searching page {page + 1} for '{town_variation}'...")
        results = get_google_results(f"{town_variation} history OR news", page)
        print(f"Found {len(results)} search results")
        
        for result in results:
            link = result.get("link")
            if not link:
                continue
            
            # Check if we already have this URL to avoid duplicates
            existing_urls = {article["url"] for article in scraped_articles}
            if link in existing_urls:
                print(f"Skipping duplicate: {link}")
                continue
                
            print(f"Scraping: {link}")
            data = scrape_url(link)
            if data:
                scraped_articles.append(data)
            time.sleep(1.5)  # Avoid hammering sites
        
        # Add extra delay between pages for each variation
        time.sleep(2)
    
    # Add longer delay between different town name variations
    time.sleep(3)

# 5. Save to file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(scraped_articles, f, indent=2, ensure_ascii=False)

print(f"Done. {len(scraped_articles)} articles saved to {OUTPUT_FILE}")
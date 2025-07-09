import os
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from serpapi import GoogleSearch
import time
import json

# 1. Config
TOWN_NAME = "Seneca"
SERP_API_KEY = "YOUR_SERPAPI_KEY"  # Get one from https://serpapi.com/
NUM_PAGES = 2  # Each page returns ~10 results

# Output file
OUTPUT_FILE = f"{TOWN_NAME.replace(' ', '_')}_compiled_articles.json"
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
for page in range(NUM_PAGES):
    print(f"Searching page {page + 1}...")
    results = get_google_results(f"{TOWN_NAME} history OR news", page)
    for result in results:
        link = result.get("link")
        if not link:
            continue
        print(f"Scraping: {link}")
        data = scrape_url(link)
        if data:
            scraped_articles.append(data)
        time.sleep(1.5)  # Avoid hammering sites

# 5. Save to file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(scraped_articles, f, indent=2, ensure_ascii=False)

print(f"Done. {len(scraped_articles)} articles saved to {OUTPUT_FILE}")
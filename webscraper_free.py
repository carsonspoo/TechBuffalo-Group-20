import requests
import bs4
import certifi
import urllib3
import json
import time
from newspaper import Article

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Default Google Search Url
url = 'https://google.com/search?q='

# Customized Search Keywords (matching the paid version)
town_variations = [
    "Seneca-Babcock",
    "Seneca Babcock", 
    "seneca-babcock",
    "seneca babcock"
]

# Output file
OUTPUT_FILE = "compiled_articles.json"
scraped_articles = []

# Function to scrape article content (same as paid version)
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

# Main scraping loop
for town_variation in town_variations:
    print(f"\n=== Searching for: {town_variation} ===")
    
    # Construct search query
    search_query = f"{town_variation} history OR news"
    
    # Fetch URL Request Data
    request_result = requests.get(url + search_query, verify=False)
    
    # Creating Soup from the fetched request
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    
    # Find all search result links
    link_elements = soup.find_all("a")
    
    print(f"Processing search results for '{town_variation}'...")
    
    for link_element in link_elements:
        href = link_element.get('href')
        if not href or not href.startswith('/url?q='):
            continue
            
        # Extract the actual URL from Google's redirect
        actual_url = href.split('/url?q=')[1].split('&')[0]
        
        # Skip non-http URLs
        if not actual_url.startswith('http'):
            continue
            
        # Check if we already have this URL to avoid duplicates
        existing_urls = {article["url"] for article in scraped_articles}
        if actual_url in existing_urls:
            print(f"Skipping duplicate: {actual_url}")
            continue
            
        print(f"Scraping: {actual_url}")
        data = scrape_url(actual_url)
        if data:
            scraped_articles.append(data)
        time.sleep(1.5)  # Avoid hammering sites
    
    # Add delay between different town name variations
    time.sleep(3)

# Save to file (same format as paid version)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(scraped_articles, f, indent=2, ensure_ascii=False)

print(f"Done. {len(scraped_articles)} articles saved to {OUTPUT_FILE}")

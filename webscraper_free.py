import requests
from bs4 import BeautifulSoup

# Default Bing Search URL
url = 'https://bing.com/search?q='

# Customized Search Keywords
events = "senecababcock neighborhood buffalo "
events = events.replace(' ', '%20')

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

# Fetch URL Request Data
try:
    request_result = requests.get(url + events, headers=headers, timeout=10)
    request_result.raise_for_status()
except requests.RequestException as e:
    print("Error fetching Bing search results:", e)
    exit(1)

# Creating Soup from the fetched request
soup = BeautifulSoup(request_result.text, "html.parser")

# Grab all major headings from search result
heading_object = soup.find_all('h2')

urls = []
# Iterate and print through result_headings
for info in heading_object:
    a_tag = info.find('a')
    if a_tag and a_tag.get('href'):
        urls.append(a_tag.get('href'))
        print("Title:", info.get_text())
        print("URL:", a_tag['href'])
        print("----------")

print(urls)

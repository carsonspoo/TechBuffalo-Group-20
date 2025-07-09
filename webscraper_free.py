import requests
import bs4
import certifi
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Default Google Search Url
url = 'https://google.com/search?q='

# Customized Search Keywords
events = ["senecababcock"]

# Fetch URL Request Data
request_result = requests.get(url + events, verify=False)

# Creating Soup from the fetched request
soup = bs4.BeautifulSoup(request_result.text, "html.parser")
# print(soup)

# Grab all major headings from search result
heading_object = soup.find_all("h3")

# Iterate and print through result_headings
for info in heading_object:
    print(info.text)
    print("-----------")

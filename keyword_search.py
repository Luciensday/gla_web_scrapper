import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict

# Function to search for keyword in webpage content
def search_keyword_in_webpage(content, keyword):
    occurrences = len(re.findall(keyword, content, re.IGNORECASE))
    return occurrences

# Main block of code to perform the task
sitemap_url = "https://www.london.gov.uk/sitemap.xml?page=1"
sitemap_content = requests.get(sitemap_url, timeout=10).text
soup = BeautifulSoup(sitemap_content, "xml")
urls = [loc.text for loc in soup.find_all("loc")]
urls = urls[0:10]

keyword = input("Enter the keyword or phrase to search for: ")
results = defaultdict(int)
total_count = 0


for url in urls:
    response = requests.get(url)
    webpage_content = response.text

    soup = BeautifulSoup(webpage_content, "html.parser")
    body_content = soup.get_text()

    occurrences = search_keyword_in_webpage(body_content, keyword)
    if occurrences > 0:
                results[url] = occurrences
                total_count += occurrences
   

# Output report
print(f"Total occurrences of '{keyword}': {total_count}")
for url, occurrences in results.items():
        print(f"{url}: {occurrences} occurrences")



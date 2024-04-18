import requests
from bs4 import BeautifulSoup

sitemap_url = "https://www.london.gov.uk/sitemap.xml?page=1"
response = requests.get(sitemap_url)
sitemap_content = response.text



soup = BeautifulSoup(sitemap_content, "xml")
urls = [loc.text for loc in soup.find_all("loc")]
urls = urls[0:10]

print(urls)


search_keyword = input("Enter the keyword or phrase to search for: ")


total_count = 0
found_urls = []

for url in urls:
    response = requests.get(url)
    webpage_content = response.text

    soup = BeautifulSoup(webpage_content, "html.parser")
    body_content = soup.get_text()

    count = body_content.lower().count(search_keyword.lower())
    if count > 0:
        total_count += count
        found_urls.append(url)

print(f"Total occurrences of '{search_keyword}': {total_count}")
print("URLs where the keyword was found:")
for url in found_urls:
       print(url)
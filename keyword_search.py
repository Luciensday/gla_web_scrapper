import requests
from bs4 import BeautifulSoup


# Function to fetch URLs from XML sitemap
sitemap_url = "https://www.london.gov.uk/sitemap.xml?page=1"
sitemap_content = requests.get(sitemap_url, timeout=10).text

# Parsing the response with xml parser 
soup = BeautifulSoup(sitemap_content, "xml")
urls = [loc.text for loc in soup.find_all("loc")]
urls = urls[0:10]

keyword = input("Enter the keyword or phrase to search for: ")


total_count = 0
found_urls = []

for url in urls:
    response = requests.get(url)
    webpage_content = response.text

    soup = BeautifulSoup(webpage_content, "html.parser")
    body_content = soup.get_text()

    count = body_content.lower().count(keyword.lower())
    if count > 0:
        total_count += count
        found_urls.append(url)

print(f"Total occurrences of '{keyword}': {total_count}")
print("URLs where the keyword was found:")
for url in found_urls:
       print(url)

# add try catch block 
# understand asynio and multithreading 
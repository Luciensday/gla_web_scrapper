import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
from collections import defaultdict

# Function to fetch URLs from XML sitemap
async def get_urls_from_sitemap(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:  # Disable SSL certificate verification
            sitemap_content = await response.text()
            soup = BeautifulSoup(sitemap_content, 'xml')
            urls = [loc.text for loc in soup.find_all('loc')]
            urls = urls[0:10]
            return urls

# Function to fetch webpage content asynchronously
async def fetch_webpage_content(session, url):
    async with session.get(url, ssl=False) as response:  # Disable SSL certificate verification
        webpage_content = await response.text()
        soup = BeautifulSoup(webpage_content, "html.parser")
        body_content = soup.get_text()
        return body_content

# Function to search for keyword in webpage content
def search_keyword_in_webpage(content, keyword):
    occurrences = len(re.findall(keyword, content, re.IGNORECASE))
    return occurrences

# Main function to perform the task

search_keyword = input("Enter the keyword or phrase to search for: ")

async def main():

    sitemap_url = "https://www.london.gov.uk/sitemap.xml?page=1"
    keyword = search_keyword
    urls = await get_urls_from_sitemap(sitemap_url)

    #create empty dictionary using defaultdic
    results = defaultdict(int)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = fetch_webpage_content(session, url)
            tasks.append(task)

        # gather is run all the tasks concurrently
        all_fetched_content = await asyncio.gather(*tasks)

        count = sum(content.lower().count(keyword.lower()) for content in all_fetched_content)

        for url, content in zip(urls, all_fetched_content):
        
            occurrences = search_keyword_in_webpage(content, keyword)
            if occurrences > 0:
                results[url] = occurrences

    # Output report
    
    print(f"Total occurrences of '{keyword}': {count}")
    for url, occurrences in results.items():
        print(f"{url}: {occurrences} occurrences")

if __name__ == "__main__":
    asyncio.run(main())
import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
from collections import defaultdict

# Function to fetch URLs from XML sitemap
async def get_urls_from_sitemap(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:  # Disable SSL certificate verification
            data = await response.text()
            soup = BeautifulSoup(data, 'xml')
            urls = [loc.text for loc in soup.find_all('loc')]
            urls = urls[0:10]
            print(urls)
            return urls

# Function to fetch webpage content asynchronously
async def fetch_webpage_content(session, url):
    async with session.get(url, ssl=False) as response:  # Disable SSL certificate verification
        return await response.text()

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

    results = defaultdict(int)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = fetch_webpage_content(session, url)
            tasks.append(task)
        # gather is run all the tasks concurrently.  
        fetched_content = await asyncio.gather(*tasks)

        for url, content in zip(urls, fetched_content):
            occurrences = search_keyword_in_webpage(content, keyword)
            if occurrences > 0:
                results[url] = occurrences

    # Output report
    
    print(f"Keyword '{keyword}' was found in the following URLs:")
    for url, occurrences in results.items():
        print(f"{url}: {occurrences} occurrences")

if __name__ == "__main__":
    asyncio.run(main())
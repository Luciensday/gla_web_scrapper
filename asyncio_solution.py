import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
from collections import defaultdict

# Function to search for keyword in webpage content
def search_keyword_in_webpage(body_content, keyword):
    occurrences = len(re.findall(keyword, body_content, re.IGNORECASE))
    return occurrences 

# Function to fetch URLs from XML sitemap
async def get_urls_from_sitemap(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:  # Disable SSL certificate verification
                sitemap_content = await response.text()
                soup = BeautifulSoup(sitemap_content, 'xml')
                urls = [loc.text for loc in soup.find_all('loc')]
                urls = urls[0:100] #it will run about 3 sec for 100 links
                return urls
    except aiohttp.ClientError as e:
        print(f"Error fetching sitemap: {e}")
        return []

# Function to fetch webpage of each link content asynchronously
async def fetch_webpage_content(session, url):
    try:
        async with session.get(url, ssl=False) as response:  
            webpage_content = await response.text()
            soup = BeautifulSoup(webpage_content, "html.parser")
            body_content = soup.get_text()
            return body_content
    except aiohttp.ClientError as e:
            print(f"Error fetching URL {url}: {e}")
            return ""


# Main function to perform the task
async def main():

    sitemap_url = "https://www.london.gov.uk/sitemap.xml?page=1"
    urls = await get_urls_from_sitemap(sitemap_url)

    if not urls:
        print("No URLs found in sitemap. Exiting.")
        return

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = fetch_webpage_content(session, url)
            tasks.append(task)

        # gather is run all the tasks concurrently
        all_fetched_content = await asyncio.gather(*tasks)

     
        keyword = input("Enter the keyword or phrase to search for: ")
        results = defaultdict(int)
        total_count = 0

        for url, body_content in zip(urls, all_fetched_content):
            occurrences = search_keyword_in_webpage(body_content, keyword)
            if occurrences > 0:
                results[url] = occurrences
                total_count += occurrences

    # Output report
    
    print(f"Total occurrences of '{keyword}': {total_count}")
    for url, occurrences in results.items():
        print(f"{url}: {occurrences} occurrences")

if __name__ == "__main__":
    asyncio.run(main())
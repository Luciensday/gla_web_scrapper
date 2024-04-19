# Web Scraping Project and Performance Comparison

## Getting Started
1. Set up a Python virtual environment by running the following command in the terminal:
    ```
    python3 -m venv venv2934
    ```
2. Activate the virtual environment:
    ```
    source venv2934/bin/activate
    ```
3. Install all dependencies within the virtual environment:
    ```
    pip3 install -r requirements.txt
    ```

## Optimized vs. Unoptimized Solution
### 1. Optimized Solution (Asyncio)
#### Running Time
3 seconds / 100 URLs (for this project)

#### Thought Process
After evaluating three options for optimization, Asyncio is the most suitable solution. The three options considered are:
- **Asyncio:** Preferred for managing many waiting tasks, particularly effective in solving I/O bottlenecks.
- **Multiprocessing:** Maximizes performance on CPU-intensive tasks, suitable for solving CPU-bound problems. However, it may cause overload and is not ideal for lightweight processes.
- **Threading:** Suitable for parallel tasks that share data with minimal CPU usage. However, in this project, threads could be cumbersome to manage and are not the best fit.



```python
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = fetch_webpage_content(session, url)
            tasks.append(task)

        # gather is run all the tasks concurrently
        all_fetched_content = await asyncio.gather(*tasks)

```


The key differences in the optimized solution are:
- Usage of `aiohttp` instead of the `requests` library because `aiohttp` can handle asynchronous data fetching efficiently.
- Instead of processing tasks upon completion of others, `asyncio` allows us to execute multiple asynchronous functions concurrently to optimize performance by overcoming I/O bottlenecks.
- The code snippet above (`await asyncio.gather(*task)`) executes all tasks on the list concurrently.

### 2. Unoptimized Solution (Requests)
#### Running Time
124 seconds / 100 URLs (for this project)

#### Thought Process
- This option utilizes the `requests` library.
    - Cons: `requests` is not designed for asynchronous processes.
    - Pros: `requests.get(url, timeout=10)` allows us to set a timeout limit to prevent undue load. (as per below image)
```python
    sitemap_content = requests.get(sitemap_url, timeout=10).text
```


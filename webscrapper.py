import asyncio
import multiprocessing
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
from markdownify import markdownify as md

async def scrape_to_scrapeddata(url, name):
    """Function to scrape a webpage and return the data as a ScrapedData object."""
    crawler = PlaywrightCrawler(max_requests_per_crawl=5, headless=True)
    markdown_content = ""

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        nonlocal markdown_content # Access the markdown_content variable from the outer scope
        await context.page.wait_for_load_state('networkidle')
        content = await context.page.content()
        markdown_content = md(content)

    # Run the crawler for the given URL
    await crawler.run([url])
    await crawler._browser_pool._close_inactive_browsers()  # Ensure all browsers are closed

    with open(f'./markdown_file/{name}.md', 'w', encoding='utf-8') as file:
        file.write(markdown_content)

    print(f'Crawling file stored in ./markdown_file/{name}.md')

async def run_scraping_sequentially(urls):
    """Run the scraping process sequentially for a list of URLs and collect the results."""
    for url in urls:
        name_html = url.split('/')[-1]
        name = name_html.split('.')[0]
        await scrape_to_scrapeddata(url, name)

if __name__ == '__main__':
    
    urls_to_scrape = [
        'https://www.here.com/docs/bundle/maps-api-for-javascript-developer-guide/page/topics/routing.html',
        'https://www.here.com/docs/bundle/maps-api-for-javascript-developer-guide/page/topics/get-started-japan.html'
    ]
    
    # Run the scraping sequentially for the list of URLs and collect the results
    asyncio.run(run_scraping_sequentially(urls_to_scrape))
    
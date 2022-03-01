import asyncio
import asyncio
from api import get_data, get_path_image10k


async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.flickr.com/photos/bunnygoth/9730950832/')
    await page.screenshot({'path': 'example.jpg'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

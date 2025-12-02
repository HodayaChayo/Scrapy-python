import scrapy

class GruberfarmSpider(scrapy.Spider):
    name = "gruberfarm_links_all"

    start_urls = [f"https://www.gruberfarm.com/search?items=all&page={i}" for i in range(1, 173)]

    custom_settings = {
        # Playwright
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": True,
            "slow_mo": 200,
            "args": [
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        },
        "PLAYWRIGHT_PAGE_WAIT_FOR_LOAD_STATE": "domcontentloaded",
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 25000,
        "PLAYWRIGHT_DEFAULT_SELECTOR_TIMEOUT": 8000,

        # Scrapy settings
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 5,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "ROBOTSTXT_OBEY": False,
        "COOKIES_ENABLED": False,
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",

        # Enable Playwright download handler
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
    }

    # רשימה גלובלית לאגירת כל הקישורים
    all_links = []
    counter = 0

    def parse(self, response):
        # בוחרים את כל ה-divים עם id שמתחיל ב-item_id
        divs = response.css(".wrap_boxs div[id^='item_id']")

        for div in divs:
            link = div.css("a::attr(href)").get()  # הקישור הראשון בכל div
            if link:
                self.counter += 1
                print(f"Found link {self.counter}: {link}")
                full_link = "https://www.gruberfarm.com" + link
                self.all_links.append(full_link)

        # אם זה הדף האחרון (172) מחזירים את המערך כולו
        current_page = int(response.url.split("page=")[-1])
        if current_page == 172:
            yield {"all_links": self.all_links}

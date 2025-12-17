import scrapy
import re
from urllib.parse import urlparse, urlunparse

class KonimboSpider(scrapy.Spider):
    name = "konimbo_safe"

    allowed_domains = ["www.gruberfarm.com"]
    start_urls = ["https://www.gruberfarm.com/"]

    product_urls = [
            "https://www.gruberfarm.com/items/7133932-%D7%A9%D7%9E%D7%9F-%D7%A1%D7%9C%D7%9E%D7%95%D7%9F-%D7%A0%D7%99%D7%A7%D7%95%D7%9F-N01-%D7%9C%D7%AA%D7%9E%D7%99%D7%9B%D7%94-%D7%91%D7%9B%D7%9C%D7%99%D7%95%D7%AA",
            "https://www.gruberfarm.com/items/7133933-%D7%A9%D7%9E%D7%9F-%D7%A1%D7%9C%D7%9E%D7%95%D7%9F-%D7%A0%D7%99%D7%A7%D7%95%D7%9F-N02-%D7%9C%D7%AA%D7%9E%D7%99%D7%9B%D7%94-%D7%91%D7%9E%D7%A2%D7%A8%D7%9B%D7%AA-%D7%94%D7%A2%D7%99%D7%9B%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/7133934-%D7%A9%D7%9E%D7%9F-%D7%A4%D7%A9%D7%AA%D7%9F-%D7%A0%D7%99%D7%A7%D7%95%D7%9F-N03-%D7%98%D7%91%D7%A2%D7%95%D7%A0%D7%99",
            "https://www.gruberfarm.com/items/7133935-%D7%A9%D7%9E%D7%9F-%D7%A1%D7%9C%D7%9E%D7%95%D7%9F-%D7%A0%D7%99%D7%A7%D7%95%D7%9F-N04-%D7%9C%D7%94%D7%A4%D7%97%D7%AA%D7%AA-%D7%A8%D7%99%D7%97%D7%95%D7%AA",
            "https://www.gruberfarm.com/items/7133936-%D7%A9%D7%9E%D7%9F-%D7%A1%D7%9C%D7%9E%D7%95%D7%9F-%D7%A0%D7%99%D7%A7%D7%95%D7%9F-N05-%D7%A1%D7%95%D7%A4%D7%A8-%D7%90%D7%95%D7%9E%D7%92%D7%94",
            "https://www.gruberfarm.com/items/7133937-%D7%A9%D7%9E%D7%9F-%D7%A1%D7%9C%D7%9E%D7%95%D7%9F-%D7%A0%D7%99%D7%A7%D7%95%D7%9F-N06-%D7%9C%D7%94%D7%A7%D7%9C%D7%94-%D7%9C%D7%9E%D7%A4%D7%A8%D7%A7%D7%99%D7%9D",
            "https://www.gruberfarm.com/items/6718722-%D7%9B%D7%9C%D7%99-%D7%9E%D7%99%D7%9D-%D7%95%D7%90%D7%95%D7%9B%D7%9C-%D7%93%D7%99%D7%A1%D7%A4%D7%A0%D7%A1%D7%A8-3-%D7%9C%D7%99%D7%98%D7%A8-IMAC-%D7%90%D7%99%D7%9E%D7%90%D7%A7",
            "https://www.gruberfarm.com/items/6770442-%D7%9B%D7%93%D7%95%D7%A8-%D7%9C%D7%9B%D7%9C%D7%91-%D7%A2%D7%9D-%D7%9C%D7%93-IMAC-%D7%90%D7%99%D7%9E%D7%90%D7%A7",
            "https://www.gruberfarm.com/items/6770443-%D7%9B%D7%93%D7%95%D7%A8-%D7%A7%D7%95%D7%A0%D7%92-%D7%9C%D7%9B%D7%9C%D7%91",
            "https://www.gruberfarm.com/items/6770711-%D7%A0%D7%95%D7%A8%D7%AA-%D7%94%D7%99%D7%99%D7%9C%D7%99%D7%99%D7%98-%D7%98%D7%91%D7%A2%D7%99-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770712-%D7%A0%D7%95%D7%A8%D7%AA-%D7%94%D7%99%D7%99%D7%9C%D7%99%D7%99%D7%98-%D7%99%D7%95%D7%9D-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770713-%D7%A0%D7%95%D7%A8%D7%AA-%D7%94%D7%99%D7%99%D7%9C%D7%99%D7%99%D7%98-%D7%9B%D7%97%D7%95%D7%9C-%D7%9C%D7%90%D7%A7%D7%95%D7%95%D7%A8%D7%99%D7%95%D7%9D-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770714-%D7%A0%D7%95%D7%A8%D7%AA-%D7%94%D7%99%D7%99%D7%9C%D7%99%D7%99%D7%98-%D7%9E%D7%A8%D7%99%D7%9F-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770715-%D7%A0%D7%95%D7%A8%D7%AA-%D7%94%D7%99%D7%99%D7%9C%D7%99%D7%99%D7%98-%D7%A6%D7%91%D7%A2-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770474-%D7%9B%D7%9C%D7%95%D7%91-%D7%A8%D7%A9%D7%AA-%D7%91%D7%95%D7%A7%D7%A1-%D7%A7%D7%99%D7%99%D7%9F-IMAC-%D7%90%D7%99%D7%9E%D7%90%D7%A7",
            "https://www.gruberfarm.com/items/6770479-%D7%9B%D7%9C%D7%99-%D7%90%D7%95%D7%9B%D7%9C-300-600-1000-%D7%9E-%D7%9C-%D7%90%D7%99%D7%9E%D7%90%D7%A7",
            "https://www.gruberfarm.com/items/6770480-%D7%9B%D7%9C%D7%99-%D7%90%D7%95%D7%9B%D7%9C-%D7%9B%D7%A4%D7%95%D7%9C-2X300-2X600-%D7%9E-%D7%9C-%D7%90%D7%99%D7%9E%D7%90%D7%A7",
            "https://www.gruberfarm.com/items/6770481-%D7%9B%D7%9C%D7%99-%D7%90%D7%95%D7%9B%D7%9C-%D7%99%D7%97%D7%99%D7%93-%D7%90%D7%95-%D7%9B%D7%A4%D7%95%D7%9C-%D7%9C%D7%9B%D7%9C%D7%91%D7%99%D7%9D-%D7%93%D7%90%D7%94-%D7%90%D7%99%D7%9E%D7%90%D7%A7",
            "https://www.gruberfarm.com/items/6770484-%D7%9B%D7%9C%D7%99-%D7%9E%D7%99%D7%9D-%D7%95%D7%90%D7%95%D7%9B%D7%9C-%D7%9C%D7%9B%D7%9C%D7%91-%D7%93%D7%99%D7%95%D7%95%D7%94-%D7%90%D7%99%D7%9E%D7%90%D7%A7",
            "https://www.gruberfarm.com/items/6770740-%D7%A1%D7%95%D7%A4%D7%97-%D7%A0%D7%99%D7%98%D7%A8%D7%90%D7%98-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6771532-%D7%9B%D7%9C%D7%99-%D7%9E%D7%99%D7%9D-%D7%95%D7%90%D7%95%D7%9B%D7%9C-%D7%93%D7%99%D7%A1%D7%A4%D7%A0%D7%A1%D7%A8-1-5-%D7%9C%D7%99%D7%98%D7%A8-IMAC",
            "https://www.gruberfarm.com/items/6770256-%D7%92%D7%95%D7%93%D7%99%D7%96-%D7%97%D7%91%D7%9C-%D7%93%D7%A0%D7%98%D7%9C-%D7%A6%D7%A2%D7%A6%D7%95%D7%A2-%D7%A7%D7%95%D7%A0%D7%92-%D7%9C%D7%9B%D7%9C%D7%91",
            "https://www.gruberfarm.com/items/6770769-%D7%A1%D7%99%D7%A8%D7%A7%D7%A1-%D7%91%D7%99%D7%95%D7%A4%D7%9C%D7%95-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6771046-%D7%A7%D7%95%D7%A0%D7%92-%D7%90%D7%A7%D7%A1%D7%98%D7%A8%D7%99%D7%9D-%D7%A9%D7%97%D7%95%D7%A8-%D7%9C%D7%9B%D7%9C%D7%91",
            "https://www.gruberfarm.com/items/6771047-%D7%A7%D7%95%D7%A0%D7%92-%D7%91%D7%95%D7%91%D7%AA-%D7%A7%D7%A9%D7%A8%D7%99%D7%9D-%D7%A6%D7%A4%D7%A8%D7%93%D7%A2-NK",
            "https://www.gruberfarm.com/items/6771051-%D7%A7%D7%95%D7%A0%D7%92-%D7%92%D7%95%D7%A8%D7%99%D7%9D-%D7%9C%D7%9B%D7%9C%D7%91",
            "https://www.gruberfarm.com/items/6771053-%D7%A7%D7%95%D7%A0%D7%92-%D7%95%D7%95%D7%91%D7%9C%D7%A8-%D7%9C%D7%9B%D7%9C%D7%91",
            "https://www.gruberfarm.com/items/6770543-%D7%9C%D7%95%D7%97%D7%99%D7%95%D7%AA-%D7%A7%D7%A8%D7%95%D7%99-%D7%9C%D7%90%D7%A7%D7%95%D7%95%D7%A8%D7%99%D7%95%D7%9D-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770292-%D7%92%D7%95%D7%A3-%D7%AA%D7%90%D7%95%D7%A8%D7%94-%D7%9C%D7%93-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6771064-%D7%A7%D7%95%D7%A0%D7%92-%D7%9C%D7%9B%D7%9C%D7%91-%D7%9B%D7%93%D7%95%D7%A8-%D7%90%D7%A7%D7%A1%D7%98%D7%A8%D7%99%D7%9D",
            "https://www.gruberfarm.com/items/6771065-%D7%A7%D7%95%D7%A0%D7%92-%D7%9C%D7%9B%D7%9C%D7%91-%D7%92%D7%95%D7%93%D7%99%D7%96",
            "https://www.gruberfarm.com/items/6771067-%D7%A7%D7%95%D7%A0%D7%92-%D7%A7%D7%9C%D7%90%D7%A1%D7%99%D7%A7-%D7%90%D7%93%D7%95%D7%9D-%D7%9C%D7%9B%D7%9C%D7%91",
            "https://www.gruberfarm.com/items/6737545-%D7%A7%D7%A8%D7%9E%D7%99%D7%A7%D7%94-%D7%91%D7%99%D7%95%D7%9E%D7%A7%D7%A1-%D7%9C%D7%91%D7%A0%D7%94-%D7%A4%D7%9C%D7%95%D7%91%D7%9C",
            "https://www.gruberfarm.com/items/6770570-%D7%9E%D7%93%D7%99%D7%94-PHORAX-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770827-%D7%A1%D7%A4%D7%95%D7%92-%D7%91%D7%99%D7%95%D7%A1%D7%9C-%D7%92%D7%A1-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770828-%D7%A1%D7%A4%D7%95%D7%92-%D7%91%D7%99%D7%95%D7%A1%D7%9C-%D7%A2%D7%93%D7%99%D7%9F-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770829-%D7%A1%D7%A4%D7%95%D7%92-%D7%9C%D7%A4%D7%99%D7%9C%D7%98%D7%A8-%D7%A4%D7%9C%D7%95%D7%91%D7%9C",
            "https://www.gruberfarm.com/items/6729358-%D7%90%D7%A7%D7%95%D7%95%D7%A8%D7%99%D7%95%D7%9D-%D7%92-%D7%90%D7%95%D7%95%D7%9C-%D7%A4%D7%A8%D7%99%D7%9E%D7%95-70",
            "https://www.gruberfarm.com/items/6771090-%D7%A7%D7%99%D7%98-2-%D7%AA%D7%95%D7%9E%D7%9B%D7%99%D7%9D-%D7%93%D7%91%D7%A7-%D7%9C%D7%A8%D7%99%D7%95-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6737557-%D7%A8%D7%90%D7%A9-%D7%9B%D7%97-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770595-%D7%9E%D7%95%D7%A0%D7%95%D7%9C%D7%95%D7%A7%D7%A1-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770348-%D7%93%D7%95%D7%90%D7%9C%D7%95%D7%A7%D7%A1-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770861-%D7%A4%D7%95%D7%9C%D7%99%D7%A4%D7%93-%D7%A7%D7%93%D7%9D-%D7%A1%D7%99%D7%A0%D7%95%D7%9F-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770864-%D7%A4%D7%95%D7%A1%D7%98%D7%A8-2-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770865-%D7%A4%D7%95%D7%A1%D7%98%D7%A8-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770871-%D7%A4%D7%97%D7%9D-%D7%A4%D7%A2%D7%99%D7%9C-2-%D7%99%D7%97%D7%99%D7%93%D7%95%D7%AA-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770616-%D7%9E%D7%97%D7%A1%D7%95%D7%9D-%D7%A0%D7%99%D7%99%D7%9C%D7%95%D7%9F-%D7%9C%D7%9B%D7%9C%D7%91-%D7%9E%D7%95%D7%A1%D7%A8%D7%95%D7%9C%D7%94-%D7%90%D7%99%D7%9E%D7%90%D7%A7",
            "https://www.gruberfarm.com/items/6770872-%D7%A4%D7%97%D7%9D-%D7%A7%D7%9C%D7%99%D7%A8-%D7%91%D7%9C%D7%95-%D7%9C%D7%90%D7%A7%D7%95%D7%95%D7%A8%D7%99%D7%95%D7%9D-Clear-blue",
            "https://www.gruberfarm.com/items/6770617-%D7%9E%D7%97%D7%A1%D7%95%D7%9D-%D7%A4%D7%9C%D7%A1%D7%98%D7%99%D7%A7-%D7%9C%D7%9B%D7%9C%D7%91-%D7%92%D7%A8%D7%95%D7%91%D7%A8-%D7%A4%D7%90%D7%A8%D7%9D",
            "https://www.gruberfarm.com/items/6770377-%D7%94%D7%A7%D7%95%D7%A1-%D7%A0%D7%95%D7%A8%D7%AA-UV-Haqos",
            "https://www.gruberfarm.com/items/6770404-%D7%98%D7%91%D7%A2%D7%95%D7%AA-%D7%94%D7%99%D7%93%D7%95%D7%A7-%D7%9C%D7%A0%D7%95%D7%A8%D7%94-%D7%92-%D7%90%D7%95%D7%95%D7%9C",
            "https://www.gruberfarm.com/items/6770157-%D7%90%D7%9C%D7%95%D7%A1-1-%D7%A0%D7%99%D7%98%D7%A8%D7%90%D7%98",
            "https://www.gruberfarm.com/items/6770158-%D7%90%D7%9C%D7%95%D7%A1-2-%D7%A4%D7%95%D7%A1%D7%A4%D7%98",
            "https://www.gruberfarm.com/items/6770159-%D7%90%D7%9C%D7%95%D7%A1-3-%D7%90%D7%A9%D7%9C%D7%92%D7%9F",
            "https://www.gruberfarm.com/items/6770160-%D7%90%D7%9C%D7%95%D7%A1-4-%D7%91%D7%A8%D7%96%D7%9C",
            "https://www.gruberfarm.com/items/6770161-%D7%90%D7%9C%D7%95%D7%A1-5-%D7%9E%D7%99%D7%A7%D7%A8%D7%95-%D7%90%D7%9C%D7%9E%D7%A0%D7%98",
            "https://www.gruberfarm.com/items/6770162-%D7%90%D7%9C%D7%95%D7%A1-6-%D7%A8%D7%99%D7%92%D7%99%D7%A0%D7%A8%D7%94",
            "https://www.gruberfarm.com/items/6770675-%D7%9E%D7%A7%D7%A8%D7%9F-%D7%9E%D7%9C%D7%95%D7%98%D7%A9-%D7%92-%D7%90%D7%95%D7%95%D7%9C-%D7%94%D7%99-%D7%9C%D7%99%D7%99%D7%98",
            "https://www.gruberfarm.com/items/6770679-%D7%9E%D7%A9%D7%90%D7%91%D7%94-%D7%9C%D7%90%D7%A7%D7%95%D7%95%D7%A8%D7%99%D7%95%D7%9D-%D7%98%D7%98%D7%A8%D7%94",
        ]

    length = len(product_urls)
    # visited url cache
    visited_urls = set()

    custom_settings = {
        # Playwright
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",

        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": True,
            "slow_mo": 200,
            # מניעת תקיעה בגלל GPU או sandbox
            "args": [
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        },

        # מניעת תקיעות בגלל networkidle
        "PLAYWRIGHT_PAGE_WAIT_FOR_LOAD_STATE": "load",

        # Timeout קשיח לכל ניווט
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 50000,

        # Timeout לבחירת סלקטורים (במקרה שהדף לא מציג אלמנט)
        "PLAYWRIGHT_DEFAULT_SELECTOR_TIMEOUT": 8000,

        # SCRAPY SETTINGS
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 5,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "ROBOTSTXT_OBEY": False,

        # Disable cookies
        "COOKIES_ENABLED": False,

        # למנוע הצטברות דפים פתוחים שגורמת לתקיעה אחרי זמן
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_REQUEST_HANDLER": "konimbo_safe.request_handler",
        "PLAYWRIGHT_PROCESS_REQUEST_HEADERS": None,
        "PLAYWRIGHT_PROCESS_REQUEST_BODY": None,
    }


    # -------------------------
    # Utility
    # -------------------------

    def start_requests(self):
        for idx, url in enumerate(self.product_urls, start=1):
            yield scrapy.Request(
            url,
            callback=self.extract_product_details,
            meta={"playwright": True, "playwright_include_page": True, "counter": idx},
            )

    async def request_handler(self, route, request):
        blocked_domains = [
            "google-analytics.com",
            "facebook.com",
            "cdn.equalweb.com", 
            "googleadservices.com",
            "youtube.com", 
        ]
        
        # 1. חסימת דומיינים למעקב ופרסומות
        if any(domain in request.url for domain in blocked_domains):
            await route.abort()
            return
        
        # 3. המשך כרגיל עבור כל בקשה אחרת (HTML, CSS, JS של האתר)
        await route.continue_()


    # -------------------------
    # Extract product details
    # -------------------------

    async def extract_product_details(self, response):
        print("in product ======================================  Extracting product details from:", response.url)
        print(f"Processing URL *****======****** {response.meta.get("counter")}/{self.length}: {response.url}")
        page = response.meta["playwright_page"]
        if not page:
            return
        
        is_parent_product = False
        try:
            # נמתין עד 5 שניות להופעת האלמנט .son_items
            await page.wait_for_selector("table.son_items", timeout=5000)
            is_parent_product = True
        except:
            pass # אם לא נמצא, is_parent_product נשאר False
            
        # המתן לגלריה
        try:
            await page.wait_for_selector("#lightSlider .lslide img", timeout=8000)
        except:
            pass

        try:
            # --- חילוץ נתונים משותפים לכל סוגי המוצרים (Playwright) ---
            img_urls = await page.eval_on_selector_all(
                "#lightSlider .lslide img",
                "nodes => nodes.map(n => n.src)"
            )
            img_urls = [img.replace('/large/', '/extra_large/') for img in img_urls]
            image_filenames = [url.split("/")[-1] for url in img_urls]
            
            locator = page.locator("#lightSlider li.video_bg.lslide")
            video_url = None
            if await locator.count() > 0:
                video_url = await locator.evaluate("node => node.getAttribute('data-src')")
            else:
                video_url = None 

            normal_video_url = None
            if video_url:
                if "/embed/" in video_url:
                    video_id = video_url.split("/embed/")[1].split("?")[0]
                    normal_video_url = f"https://www.youtube.com/watch?v={video_id}"
                else:
                    normal_video_url = video_url
            
            # --- חילוץ נתונים משותפים לכל סוגי המוצרים (Scrapy Response) ---
            breadcrumbs_href = response.css("#bread_crumbs a ::attr(href)").getall()
            breadcrumbs_href = ["https://www.gruberfarm.com" + href for href in breadcrumbs_href]
            breadcrumbs_text = response.css("#bread_crumbs a ::text").getall()
            category_url = breadcrumbs_href[2] if len(breadcrumbs_href) >= 3 else ""
            category_name = breadcrumbs_text[2] if len(breadcrumbs_text) >= 3 else ""
            # ... (המשך חילוץ כל שאר הנתונים הסטטיים: category_url2, category_name2, וכו') ...
            category_url2 = breadcrumbs_href[3] if len(breadcrumbs_href) >= 4 else ""
            category_name2 = breadcrumbs_text[3] if len(breadcrumbs_text) >= 4 else ""
            category_url3 = breadcrumbs_href[4] if len(breadcrumbs_href) >= 5 else ""
            category_name3 = breadcrumbs_text[4] if len(breadcrumbs_text) >= 5 else ""
            category_url4 = breadcrumbs_href[5] if len(breadcrumbs_href) >= 6 else ""
            category_name4 = breadcrumbs_text[5] if len(breadcrumbs_text) >= 6 else ""
            product_url = response.url
            
            product_name_base = response.css("#item_current_title h1 span::text").get()
            if product_name_base:
                product_name_base = product_name_base.strip()
            
            product_SKU_base = response.css(".code_item ::text").get()
            if product_SKU_base:
                product_SKU_base = product_SKU_base.strip()
            
            final_price_base = response.css('#item_show_price .price_value ::text').get()
            if final_price_base:
                final_price_base = final_price_base.replace("₪", "").strip()
            
            original_price_base = response.css('#item_details .item_show_origin_price .origin_price_number ::text').get()
            if original_price_base:
                original_price_base = original_price_base.replace("₪", "").strip()
                
            description = response.css("#item_current_sub_title span ::text").getall()
            description_html = self.clean_style_html(response.css("#item_current_sub_title span").get())
            more_description = response.css(".specifications .desc ::text").getall()
            more_description_html = self.clean_style_html(response.css(".specifications .desc").get())
            colors = response.css('#item_upgrades_top select.inventory option ::text').getall()
            
            # יצירת מילון בסיס
            base_product = {
                        "category_url": category_url,
                        "category_name": category_name,
                        "category_url2": category_url2,
                        "category_name2": category_name2,
                        "category_url3": category_url3,
                        "category_name3": category_name3,
                        "category_url4": category_url4,
                        "category_name4": category_name4,
                        "product_url": product_url,
                        "product_name": product_name_base,
                        "product_SKU": product_SKU_base,
                        "final_price": final_price_base,
                        "original_price": original_price_base,
                        "images_links": '\n'.join(img_urls),
                        "images_names": '\n'.join(image_filenames),
                        "youtube_link": normal_video_url,
                        "description": ' '.join(description),
                        "description_html": description_html,
                        "more_description": ' '.join(more_description),
                        "more_description_html": more_description_html,
                        "colors": '\n'.join(colors),
                        # "son_name": '',
                        # "son_sku": '',
                        # "son_final_price": '',
                        # "son_original_price": '',
                        # "son_image": '',
                        # "son_image_name": '',
                        "sons_SKUs": '',
                        "is_son_product": '',
                    }


            # ----------------------------------------------
            # 2. פיצול הלוגיקה: מוצרי בן מול מוצר יחיד
            # ----------------------------------------------

            if is_parent_product:
                # א. מקרה: מוצר אב עם מוצרי בן (יש לולאה ו-yield מרובים)
                
                son_items_data = await page.eval_on_selector_all(
                    "table.son_items tr[data-id]",
                    """nodes => nodes.map(node => {
                        const imgElement = node.querySelector('.son_image img');
                        const imageUrl = imgElement ? imgElement.getAttribute('src') : null;
                        
                        // מחיר מקורי (מופיע ב-td.son_origin_price)
                        const originalPriceElement = node.querySelector('td.son_origin_price');
                        const originalPriceText = originalPriceElement ? originalPriceElement.innerText.trim() : null;
                        
                        // מחיר סופי (מופיע בתוך span הראשון ב-td.son_price)
                        const finalPriceElement = node.querySelector('.son_price span:first-child');
                        const finalPriceText = finalPriceElement ? finalPriceElement.innerText.trim() : null;
                        
                        return {
                            son_image: imageUrl ? imageUrl.replace('/large/', '/extra_large/') : '',
                            son_sku: node.querySelector('.son_code').innerText.trim(),
                            son_name: node.querySelector('.son_title').innerText.trim(),
                            son_original_price: originalPriceText ? originalPriceText.replace('₪', '').trim() : '',
                            son_final_price: finalPriceText ? finalPriceText.replace('₪', '').trim() : '',
                        };
                    })""",
                )
                
                # שליחת שורות נפרדות לכל מוצר בן
                base_product["is_son_product"] = False
                base_product["sons_SKUs"] = '\n'.join([son["son_sku"] for son in son_items_data])
                yield base_product.copy() # yield של מוצר האב עצמו
                for son in son_items_data:
                    final_item = base_product.copy() 
                    
                    # דריסה של שדות האב עם נתוני הבן
                    final_item["product_name"] = son["son_name"]
                    final_item["product_SKU"] = son["son_sku"]
                    final_item["final_price"] = son["son_final_price"]
                    final_item["original_price"] = son["son_original_price"]
                    final_item["images_links"] = son["son_image"] + '\n' + final_item["images_links"]
                    final_item["images_names"] = (son["son_image"].split("/")[-1] if son["son_image"] else '') + '\n' + final_item["images_names"]
                    
                    # הוספת שדות עזר לזיהוי מוצר הבן, אם נדרש
                    final_item["is_son_product"] = True
                    
                    print("Extracted son product:", final_item["product_name"])
                    yield final_item
            
            
            else:
                # ב. מקרה: מוצר רגיל/אב יחיד (yield יחיד)
                
                # אין צורך לבנות מחדש את המילון, הוא כבר base_product
                product = base_product.copy()
                
                # הוספת שדות עזר ריקים למוצר רגיל כדי לשמור על מבנה אחיד
                product["is_son_product"] = False
                
                print("Extracted product:", product)
                yield product
                
        
        finally:
            # *** קטע קוד זה יסגור את אובייקט ה-Page ***
            await page.close()


    def clean_style_html(self, selected_element):

            if selected_element:
                # Regular expressions to remove 'style' and 'class' attributes
                selected_element = re.sub(r'\s*style="[^"]*"', '', selected_element)  # Remove 'style' attributes
                selected_element = re.sub(r'\s*class="[^"]*"', '', selected_element)  # Remove 'class' attributes
                selected_element = re.sub(r'\s*dir="[^"]*"', '', selected_element)  # Remove 'dir' attributes
                selected_element = re.sub(r'<iframe.*?>.*?</iframe>', '', selected_element, flags=re.DOTALL)


                return selected_element
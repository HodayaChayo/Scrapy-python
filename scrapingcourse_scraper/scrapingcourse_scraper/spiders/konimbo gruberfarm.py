import scrapy
import random
import asyncio
from urllib.parse import urlparse, urlunparse

class KonimboSpider(scrapy.Spider):
    name = "konimbo_safe"

    allowed_domains = ["www.gruberfarm.com"]
    start_urls = ["https://www.gruberfarm.com/"]

    # visited url cache
    visited_urls = set()

    custom_settings = {
        # Playwright
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False,
            "slow_mo": 200,
        },
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 25000,

        # SCRAPY SETTINGS
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 8,                   # מינימום 8 שניות
        "RANDOMIZE_DOWNLOAD_DELAY": True,      # רנדומלי עד ~15 שניות
        "ROBOTSTXT_OBEY": False,

        # Disable cookies (מעולה נגד אנטי בוט)
        "COOKIES_ENABLED": False,
    }

    # -------------------------
    # Utility
    # -------------------------

    def clean_url(self, url):
        parsed = urlparse(url)
        return urlunparse(parsed._replace(query="", fragment=""))

    def is_valid_url(self, url):
        return (
            url.startswith("https://www.gruberfarm.com")
            and "mailto:" not in url
            and ".jpg" not in url
            and ".png" not in url
            and ".pdf" not in url
            and "#" not in url
        )

    def is_product_page(self, url):
        return "/items/" in url

    # -------------------------
    # Main parse
    # -------------------------

    def parse(self, response):
        cleaned = self.clean_url(response.url)
        if cleaned in self.visited_urls:
            return

        self.visited_urls.add(cleaned)
        # ⚠️ קטע יצירת ה-Request הכפול ל-extract_product_details הוסר מכאן ⚠️

        # מציאת לינקים פוטנציאליים
        links = response.css("a::attr(href)").getall()

        for link in links:
            url = response.urljoin(link)
            url = self.clean_url(url)

            if not self.is_valid_url(url):
                continue

            if url in self.visited_urls:
                continue

            # הגבלת עומק: אל תלכי ליותר מ-3 רמות
            if url.count("/") - 3 > 3:
                continue

            # קביעת callback ו-meta בהתאם לסוג הדף
            if self.is_product_page(url):
                # אם זה דף מוצר: קרא ל-extract_product_details וצרף את אובייקט ה-page
                callback_func = self.extract_product_details
                meta_data = {"playwright": True, "playwright_include_page": True,}
            else:
                # אם זה דף רגיל: המשך לסרוק ב-parse
                callback_func = self.parse
                meta_data = {"playwright": True}

            yield scrapy.Request(
                url,
                callback=callback_func,
                meta=meta_data,
            )

    # -------------------------
    # Extract product details
    # -------------------------

    async def extract_product_details(self, response):
        print("in product ======================================  Extracting product details from:", response.url)
        page = response.meta["playwright_page"]
        if not page:
            return
        try:
            # המתן לגלריה
            try:
                await page.wait_for_selector("#lightSlider .lslide img", timeout=8000)
            except:
                pass

            # שלוף את כל התמונות מתוך הסלקטור
            img_urls = await page.eval_on_selector_all(
                "#lightSlider .lslide img",
                "nodes => nodes.map(n => n.src)"
            )
            
            img_urls = [img.replace('/large/', '/extra_large/') for img in img_urls]
            # --- חילוץ שמות קבצים ---
            image_filenames = [url.split("/")[-1] for url in img_urls]
            
            # --- בדיקת סרטון ביוטיוב ---
            locator = page.locator("#lightSlider li.video_bg.lslide")
            
            # 2. בדוק אם האלמנט קיים לפני שמנסים לחלץ את התכונה
            if await locator.count() > 0:
                video_url = await locator.evaluate("node => node.getAttribute('data-src')")
            else:
                video_url = None # הגדר None אם לא נמצא סרטון

            # אם נמצא סרטון, ממירים מקישור embed לקישור רגיל
            normal_video_url = None

            if video_url:
                # video_url יהיה למשל: https://www.youtube.com/embed/UBU-Fwuv6jc
                if "/embed/" in video_url:
                    video_id = video_url.split("/embed/")[1].split("?")[0]
                    normal_video_url = f"https://www.youtube.com/watch?v={video_id}"
                else:
                    # fallback — אם יתפתחו פורמטים אחרים
                    normal_video_url = video_url
            
            breadcrumbs_href = response.css("#bread_crumbs  a ::attr(href)").getall()
            breadcrumbs_href = ["https://www.gruberfarm.com" + href for href in breadcrumbs_href]
            breadcrumbs_text = response.css("#bread_crumbs  a ::text").getall()
            category_url = breadcrumbs_href[2] if len(breadcrumbs_href) >= 3 else ""
            category_name = breadcrumbs_text[2] if len(breadcrumbs_text) >= 3 else ""
            category_url2 = breadcrumbs_href[3] if len(breadcrumbs_href) >= 4 else ""
            category_name2 = breadcrumbs_text[3] if len(breadcrumbs_text) >= 4 else ""
            category_url3 = breadcrumbs_href[4] if len(breadcrumbs_href) >= 5 else ""
            category_name3 = breadcrumbs_text[4] if len(breadcrumbs_text) >= 5 else ""
            category_url4 = breadcrumbs_href[5] if len(breadcrumbs_href) >= 6 else ""
            category_name4 = breadcrumbs_text[5] if len(breadcrumbs_text) >= 6 else ""
            product_url = response.url
            product_name = response.css("#item_current_title h1 span::text").get()
            if product_name:
                product_name = product_name.strip() 
            product_SKU = response.css(".code_item ::text").get()   
            if product_SKU:
                product_SKU = product_SKU.strip() 
            final_price = response.css('#item_show_price .price_value ::text').get().replace("₪", "").strip()
            original_price = response.css('#item_details .item_show_origin_price .origin_price_number ::text').get().replace("₪", "").strip()

            # product_imgs = response.css(".swiper-slide.productImage ::attr(data-src)").getall()    
            # product_img_names = [re.search(r'/([^/]+)$', url).group(1) for url in product_imgs if re.search(r'/([^/]+)$', url)]
            # description = response.css(".productOrVariationSpoiler .collapse ::text").getall()
            # description_html = response.css(".productOrVariationSpoiler .collapse").get()
            # if description_html:
            #     description_html = self.remove_unwanted_attributes(description_html)
            
        


            product = {
                "category_url": category_url,
                "category_name": category_name,
                "category_url2": category_url2,
                "category_name2": category_name2,
                "category_url3": category_url3,
                "category_name3": category_name3,
                "category_url4": category_url4,
                "category_name4": category_name4,
                "product_url": product_url,
                "product_name": product_name,
                "product_SKU": product_SKU,
                "final_price": final_price,
                "original_price": original_price,
                "images_links": '\n'.join(img_urls),
                "images_names": '\n'.join(image_filenames),
                "youtube_link": normal_video_url,
                # "product_img": self.extract_product_images(product_imgs),
                # "product_img_names": product_img_names,
                # "description": description,
                # "description_html": description_html
            }
            print("Extracted product:", product)

            yield product
            
        finally:
            # *** קטע קוד זה יסגור את אובייקט ה-Page ***
            await page.close()

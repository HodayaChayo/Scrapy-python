import scrapy
import re
import json
from scrapy_playwright.page import PageMethod

class SitemapSpider(scrapy.Spider):
    name = 'nike'
    allowed_domains = ['nike.com']
    visited_urls = set()  # Store visited URLs to avoid duplicates
    av_id = 1

    # Your list of product page URLs
    start_urls = [
        "https://www.nike.com/t/vomero-18-womens-road-running-shoes-7rbVWb/HM6804-104",
        "https://www.nike.com/t/pegasus-41-womens-road-running-shoes-tSbZGh/FD2723-702",
        "https://www.nike.com/t/zoom-fly-6-womens-road-racing-shoes-mcpFkg/FN8455-701",
        "https://www.nike.com/t/pegasus-plus-womens-road-running-shoes-oKT6Z9rd/HV3032-600",
        "https://www.nike.com/t/pegasus-trail-5-gore-tex-womens-waterproof-trail-running-shoes-ltkHcC/FQ0912-007",
        "https://www.nike.com/t/wildhorse-10-womens-trail-running-shoes-qZCXCb/FV2337-600",
        "https://www.nike.com/t/pegasus-trail-5-womens-trail-running-shoes-NsBQn9/DV3865-601",
        "https://www.nike.com/t/zegama-2-womens-trail-running-shoes-0RTMf0/FD5191-600",
        "https://www.nike.com/t/alphafly-3-womens-road-racing-shoes-LQX5b4/FD8315-101",
        "https://www.nike.com/t/vaporfly-4-womens-road-racing-shoes-hVz16nSu/HF6412-400",
        "https://www.nike.com/t/structure-25-womens-road-running-shoes-qpkKMs/IB7452-100",
        "https://www.nike.com/t/journey-run-womens-road-running-shoes-vKsnl4/FJ7765-700",
        "https://www.nike.com/t/run-defy-womens-road-running-shoes-rdVJVc/HM9593-001",
        "https://www.nike.com/t/pegasus-easyon-womens-road-running-shoes-mwi3rPBd/FQ7844-101",
        "https://www.nike.com/t/revolution-8-womens-road-running-shoes-X7DyH5j4/HJ8485-200",
        "https://www.nike.com/t/invincible-3-womens-road-running-shoes-pPkRKQhJ/DR2660-106",
        "https://www.nike.com/t/streakfly-2-road-racing-shoes-I1ybhouy/HF6416-600",
        "https://www.nike.com/t/quest-6-womens-road-running-shoes-5msqEn73/FD6034-501",
        "https://www.nike.com/t/free-rn-2018-womens-running-shoes-zE8Je3/942837-001",
        "https://www.nike.com/t/downshifter-13-womens-road-running-shoes-extra-wide-T2dDgQ/FZ3088-002"
]

    scraped_data = [] # in json for spliting to excel sheets

    def parse(self, response):
        # Skip if URL has already been visited
        if response.url in self.visited_urls:
            return
        self.visited_urls.add(response.url)
        

        variants = response.css('#colorway-picker-container a::attr(href)').getall()
        
        for variant in variants:
            variant_product = f"https://www.nike.com{variant}"
            yield scrapy.Request(url=variant_product, callback=self.extract_product_details, meta={"playwright": True,"playwright_include_page": True, "av_id": self.av_id})
        self.av_id += 1


    async def extract_product_details(self, response):
        page = response.meta["playwright_page"]
        await page.wait_for_load_state("networkidle")

        # 🖼️ Extract images using hover method (as you had)
        image_urls = []
        thumbs = await page.query_selector_all('div[data-testid^="Thumbnail-"]')
        print(thumbs)
        for thumb in thumbs:
            await thumb.hover()
            await page.wait_for_timeout(300)
        
        imges = await page.query_selector_all('#hero-image img')
        for img in imges:
            src = await img.get_attribute("src")
            if src and src not in image_urls:
                image_urls.append(src)

        # 🧠 Extract all other fields using Playwright
        product_url = response.url
        product_name = await page.text_content('#pdp_product_title')
        product_price = await page.text_content('#price-container span')
        product_sku = response.url.rstrip("/").split("/")[-1]
        description_element = await page.query_selector('#product-description-container')
        product_description = await description_element.inner_text() if description_element else ''
        color_elements = await page.query_selector_all('li[data-testid="product-description-color-description"]')
        color = await color_elements[-1].text_content() if color_elements else ''

        await page.close()  # close the browser tab

        yield {
            "product_url": product_url,
            "product_name": product_name.strip() if product_name else None,
            "av_id": response.meta["av_id"],
            "product_sku": product_sku,
            "product_price": product_price.strip() if product_price else None,
            "product_img": '\n'.join(image_urls),
            "product_description": product_description.strip(),
            "color": color.replace("Shown: ", "").strip(),
        }

    # async def extract_product_details(self, response):
        
    #     page = response.meta["playwright_page"]
    #     await page.wait_for_load_state("networkidle")
    #     await page.wait_for_selector('img')
        
    #     thumbnails = await page.query_selector_all('div[data-testid="ThumbnailListContainer"] div')

    #     for thumb in thumbnails:
    #         # Hover over the thumbnail to trigger the main image change
    #         await thumb.hover()
    #         await page.wait_for_timeout(500)
        
    #     img_elements = await page.query_selector_all('#hero-image img[data-testid="HeroImg"]')
    #     image_urls = []

    #     for img in img_elements:
    #         src = await img.get_attribute("src")
    #         if src:
    #             image_urls.append(src)

    #     product_url = response.url
    #     product_name = response.css('#pdp_product_title ::text').get()
    #     product_sku = response.url.rstrip("/").split("/")[-1]
    #     product_price = response.css('#price-container span ::text').get()
    #     product_description = response.css('#product-description-container').xpath('string()').get().strip()
    #     color = response.css('li[data-testid="product-description-color-description"]::text').getall()[-1]

    #     product_details = {
    #         "product_url": product_url,
    #         "product_name": product_name,
    #         "product_sku": product_sku,
    #         "product_price": product_price,
    #         "product_img": '\n'.join(image_urls),
    #         "product_description": product_description,
    #         "color": color,
    #     }

    #     yield product_details

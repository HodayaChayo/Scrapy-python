import scrapy

class SitemapSpider(scrapy.Spider):
    name = 'puma'
    allowed_domains = ['us.puma.com']
    visited_urls = set()  # Store visited URLs to avoid duplicates

    # Your list of product page URLs
    start_urls = [
        "https://us.puma.com/us/en/pd/pwr-hybrid-training-shoes-women/310477?swatch=13"
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
            yield scrapy.Request(url=variant_product, callback=self.extract_product_details)



    async def extract_product_details(self, response):
        
        page = response.meta["playwright_page"]
        await page.wait_for_load_state("networkidle")
        await page.wait_for_selector('img')
        
        thumbnails = await page.query_selector_all('div[data-testid="ThumbnailListContainer"] div')

        for thumb in thumbnails:
            # Hover over the thumbnail to trigger the main image change
            await thumb.hover()
            await page.wait_for_timeout(500)
        
        img_elements = await page.query_selector_all('#hero-image img[data-testid="HeroImg"]')
        image_urls = []

        for img in img_elements:
            src = await img.get_attribute("src")
            if src:
                image_urls.append(src)

        product_url = response.url
        product_name = response.css('#pdp_product_title ::text').get()
        product_sku = response.url.rstrip("/").split("/")[-1]
        product_price = response.css('#price-container span ::text').get()
        product_description = response.css('#product-description-container').xpath('string()').get().strip()
        color = response.css('li[data-testid="product-description-color-description"]::text').getall()[-1]

        product_details = {
            "product_url": product_url,
            "product_name": product_name,
            "product_sku": product_sku,
            "product_price": product_price,
            "product_img": '\n'.join(image_urls),
            "product_description": product_description,
            "color": color,
        }

        yield product_details

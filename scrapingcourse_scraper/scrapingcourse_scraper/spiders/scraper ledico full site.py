import scrapy
from urllib.parse import urlparse, urlunparse

class SitemapSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["ledico.com"]
    start_urls = ["https://www.ledico.com/"]

    visited_urls = set()  # Store visited URLs to avoid duplicates

    def clean_url(self, url):
        """
        Remove query parameters from the URL to ensure duplicates are avoided.
        """
        parsed = urlparse(url)  # Break URL into parts
        cleaned_url = urlunparse(parsed._replace(query=""))  # Remove the query part
        return cleaned_url

    def parse(self, response):
        # Clean the current response URL
        cleaned_url = self.clean_url(response.url)

        # Skip if URL has already been visited
        if cleaned_url in self.visited_urls:
            return
        self.visited_urls.add(response.url)  # Add the URL to the visited set

        # Check if this is a product page
        if self.is_product_page(response):
            yield self.extract_product_details(response)

        # Extract all internal links
        links = response.css("a::attr(href)").getall()
        for link in links:
            url = response.urljoin(link)
            if self.is_valid_url(url) and url not in self.visited_urls:
                yield scrapy.Request(url, callback=self.parse)

    def is_product_page(self, response):
        return bool(response.css(".product_wrapper"))

    def extract_product_details(self, response):
        product_name = response.css(".product_wrapper h1 ::text").get()
        product_url = response.url
        product_price = response.css(".product_wrapper .woocommerce-Price-amount ::text").get()
        if product_price:
            product_price = product_price.replace(u'\xa0', u'')
        product_img = response.css(".woocommerce-product-gallery__image > a::attr(href)").get()
        prosuct_description = response.css(".woocommerce-product-details__short-description").get()
        product_SKU = response.css(".sku ::text").get()

        table_rows = response.css(".technical_description-div table tr")
        table_data = {}
        for row in table_rows:
            key = row.css("td:nth-child(2) ::text").get()
            value = row.css("td:nth-child(1) ::text").get()
            if key and value:
                table_data[key.strip()] = value.strip()

        return {
            "product_url": product_url,
            "product_name": product_name,
            "prosuct_description": prosuct_description,
            "product_SKU": product_SKU,
            "product_price": product_price,
            "product_img": product_img,
            "technical_data": table_data,
        }

    def is_valid_url(self, url):
        return self.allowed_domains[0] in url and "mailto:" not in url and "#" not in url
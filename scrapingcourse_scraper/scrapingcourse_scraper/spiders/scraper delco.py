import scrapy
from urllib.parse import urlparse, urlunparse
import re

class SitemapSpider(scrapy.Spider):
    name = "scraper3"
    allowed_domains = ["delco.co.il"]
    start_urls = ["https://www.delco.co.il/"]

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
        return bool(response.css(".id_product"))

    def extract_product_details(self, response):
        product_url = response.url
        product_name = response.css(".id_product .ln1 ::text").get()
        product_name2 = response.css(".id_product .ln2 ::text").get()
        product_model = response.css(".print_product .ln1 ::text").get()
        if product_model:
            product_model = product_model.replace('דגם: ', '').strip()

        product_SKU = response.css(".print_product .ln2 ::text").get()   
        if product_SKU:
            product_SKU = product_SKU.replace('מק"ט: ', '').strip()     


        return {
            "product_url": product_url,
            "product_name": product_name,
            "product_name2": product_name2,
            "product_model": product_model,
            "product_SKU": product_SKU,
            "product_img": self.extract_product_images(response),
            "description": self.extract_box_data(response, "תיאור המוצר"),
            "technical_data": self.extract_box_data(response, "נתונים טכניים"),
            "accessories": self.extract_box_data(response, "ציוד נלווה "),
        }
    
    def extract_box_data(self, response, heading_text):
        # Find the box by its heading
        box = response.xpath(f"//div[@class='box_1' and div[@class='heading' and text()='{heading_text}']]")
        if box:
            # Extract the raw HTML content of the .ckeditor element
            html_content = box.css(".ckeditor").get()
            if html_content:
                # Regular expressions to remove 'style' and 'class' attributes
                html_content = re.sub(r'\s*style="[^"]*"', '', html_content)  # Remove 'style' attributes
                html_content = re.sub(r'\s*class="[^"]*"', '', html_content)  # Remove 'class' attributes
                html_content = re.sub(r'\s*dir="[^"]*"', '', html_content)  # Remove 'dir' attributes
                html_content = re.sub(r'<iframe.*?>.*?</iframe>', '', html_content, flags=re.DOTALL)


                return html_content
        return ""

    def extract_product_images(self, response):
        # Extract image URLs
        product_imgs = response.css(".prod_slider .overview ul li a::attr(img-original)").getall()
        # Join the image URLs into a single string, each separated by a newline
        return "https://www.delco.co.il" + "\nhttps://www.delco.co.il".join(product_imgs) if product_imgs else ""

    def is_valid_url(self, url):
        return self.allowed_domains[0] in url and "mailto:" not in url and "#" not in url
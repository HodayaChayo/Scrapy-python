import scrapy
import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from openpyxl import Workbook

class SitemapSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["yiron.co.il"]
    start_urls = ["https://yiron.co.il/"]

    visited_urls = set()  # Store visited URLs to avoid duplicates

    scraped_data = [] # in json for spliting to excel sheets
    
    # for attributes table
    table_data = {}
 

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
            data = self.extract_product_details(response)
            self.scraped_data.append(data)
            yield data

        # Extract all internal links
        links = response.css("a::attr(href)").getall()
        for link in links:
            url = response.urljoin(link)
            if self.is_valid_url(url) and url not in self.visited_urls:
                yield scrapy.Request(url, callback=self.parse)

    def is_product_page(self, response):
        return bool(response.css('div[data-elementor-type="wp-post"]'))

    def extract_product_details(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # Reset values in table_data for this product
        for key in self.table_data.keys():
            self.table_data[key] = None

        breadcrumbs_href = response.css("#breadcrumbs a ::attr(href)").getall()
        breadcrumbs_text = response.css("#breadcrumbs a ::text").getall()
        category_url = breadcrumbs_href[1] if len(breadcrumbs_href) >= 2 else ""
        category_name = breadcrumbs_text[1] if len(breadcrumbs_text) >= 2 else ""
        category_url2 = breadcrumbs_href[2] if len(breadcrumbs_href) >= 3 else ""
        category_name2 = breadcrumbs_text[2] if len(breadcrumbs_text) >= 3 else ""
        # category_url3 = breadcrumbs_href[3] if len(breadcrumbs_href) >= 4 else ""
        # category_name3 = breadcrumbs_text[3] if len(breadcrumbs_text) >= 4 else ""
        article_url = response.url
        article_name = response.css('h1.elementor-heading-title ::text').get()
        article_text = response.css('div[data-elementor-type="wp-post"] .elementor-widget-text-editor .elementor-widget-container ::text').getall()
        articleHTML = response.css('div[data-elementor-type="wp-post"] .elementor-widget-text-editor .elementor-widget-container').getall()
        if articleHTML:
            articleHTML = self.remove_unwanted_attributes(articleHTML[0])
        article_photos = response.css('div[data-elementor-type="wp-post"] .elementor-widget-text-editor .elementor-widget-container img:not([src^="data"]) ::attr(src)').getall()
        # product_price = response.css(".elementor-widget-jet-single-price .price .woocommerce-Price-amount.amount bdi ::text").getall()[1]
        # # if product_price:
        # #     product_price = product_price.replace(u'\xa0', u'')
        # product_img = response.css('.swiper-wrapper .jet-woo-product-gallery__image-item img ::attr(src)').getall()
        # product_img_names = [re.search(r'/([^/]+)$', url).group(1) for url in product_img if re.search(r'/([^/]+)$', url)]
        # attr = response.xpath("//div[@class='elementor-widget-container']/span[contains(@class, 'elementor-heading-title')]/text()")
        # product_SKU = attr[0].re(r'מק"ט:\s*(\S+)')
        # materials = attr[1].re(r'חומרים:\s*(.+)') if len(attr) > 1 else None
        # delivery_cost = attr[2].re(r'עלות הובלה:\s*(.+)') if len(attr) > 2 else None
        # delivery_and_assembly = None
        # if not delivery_cost:
        #     delivery_and_assembly = attr[2].re(r':\s*(.+)') if len(attr) > 2 else None
        # Assembly_cost = response.css('.ppom-option-label-price ::text').get()
        # Assembly_cost = Assembly_cost.strip("[]+") if Assembly_cost else None
        # colors = response.css('select[id^="pa"] option ::text').getall()[1:]
        # Assembly_instructions = response.css('.jet-listing-dynamic-link__link ::attr(href)').get()
        # description = ''.join(response.css('.jet-listing-dynamic-field__content .product ::text').getall())
        # descriptionHTML = response.css('.jet-listing-dynamic-field__content .product').getall()
        # if descriptionHTML:
        #     descriptionHTML = self.remove_unwanted_attributes(descriptionHTML[0])
    

        product_details = {
            "category_url": category_url,
            "category_name": category_name,
            "category_url2": category_url2,
            "category_name2": category_name2,
            # "category_url3": category_url3,
            # "category_name3": category_name3,
            "article_url": article_url,
            "article_name": article_name,
            "article_photos": '\n'.join(article_photos),
            "article_text": ''.join(article_text),
            "articleHTML": articleHTML,
            # "product_SKU": product_SKU,
            # "product_price": product_price,
            # "materials": materials,
            # "delivery_cost": delivery_cost,
            # "Assembly_cost": Assembly_cost,
            # "delivery_and_assembly": delivery_and_assembly,
            # "colors": '\n'.join(colors),
            # "Assembly_instructions": Assembly_instructions,
            # "product_img": '\n'.join(product_img),
            # "product_img_names": '\n'.join(product_img_names),
            # "description": description,
            # "descriptionHTML": descriptionHTML,
        }

        product_details.update(self.table_data)

        return product_details

    def is_valid_url(self, url):
        return self.allowed_domains[0] in url and "mailto:" not in url and "#" not in url
        
    def remove_unwanted_attributes(self, html):
        # Regular expression to match any HTML tag
        def clean_tag(match):
            tag_name = match.group(1)
            attributes = match.group(2)

            # Only keep attributes for <a> and <img> tags
            if tag_name in ['a', 'img']:
                return f"<{tag_name}{attributes}>"
            else:
                return f"<{tag_name}>"

        # Regex to match tags and their attributes
        regex = re.compile(r'<(\w+)(\s+[^>]*?)>')

        # Apply the regex to remove unwanted attributes
        return re.sub(regex, clean_tag, html)
        
    def closed(self, reason):
        # Called when the spider finishes scraping
        # self.export_to_excel()
        print(self.table_data)

    def export_to_excel(self):
        # Create a new Excel workbook
        workbook = Workbook()

        # Sheet 1: Main product details
        sheet1 = workbook.active
        sheet1.title = "Products"
        sheet1.append(["product_url", "product_name", "product_SKU", "product_price"])
        for item in self.scraped_data:
            sheet1.append([item["product_url"], item["product_name"], item["product_SKU"], item["product_price"]])

        # Sheet 2: categories
        sheet2 = workbook.create_sheet(title="categories")
        sheet2.append(["category_url", "category_name", "subcategory_url", "subcategory_name", "product_url", "product_name"])
        for item in self.scraped_data:
            sheet2.append([item["category_url"], item["category_name"], item["subcategory_url"], item["subcategory_name"], item["product_url"], item["product_name"]])

        # Save the workbook to a file
        workbook.save("scraped_data.xlsx")
        self.log("Data exported to scraped_data.xlsx")

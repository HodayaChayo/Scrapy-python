import scrapy
import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from openpyxl import Workbook

class SitemapSpider(scrapy.Spider):
    name = "scraper4"
    allowed_domains = ["dewalt-tools.co.il"]
    start_urls = ["https://dewalt-tools.co.il/"]

    visited_urls = set()  # Store visited URLs to avoid duplicates

    scraped_data = [] # in json for spliting to excel sheets
    
    # for attributes table
    table_data = {
    "סוג כלי": None,
    "מתח העבודה": None,
    "סוללות": None,
    "מטען": None,
    "זרימת אוויר 200 קמ'ש": None,
    "משקל": None,
    "כללי": None,
    "סוג מנוע": None,
    "ספיקת אוויר": None,
    "זרימת אוויר": None,
    "ווסת מהירות": None,
    "מהירות סיבוב": None,
    "רוחב כיסוח": None,
    "עובי חוט גיזום": None,
    "אורך כולל": None,
    "רצועה לכתף": None,
    "ויסות אלקטרוני": None,
    "מומנט סגירה מקסימאלי": None,
    "מומנט פתיחה מקסימאלי": None,
    "הינע": None,
    "הערות": None,
    "פעימות בדקה": None,
    "במזוודה קשיחה HD": None,
    "קוטר להב": None,
    "רטיטות לדקה": None,
    "מומנט פיתול": None,
    "פוטר": None,
    "קצב רטיטות": None,
    "תאורה": None,
    "תאורת לד": None,
    "מזוודה קשיחה": None,
    "עוצמת הלימה": None,
    "מצבי עבודה": None,
    "כושר קידוח": None,
    "מטען מהיר": None,
    "מהירויות עבודה": None,
    "ציר הברגה": None,
    "התנעה": None,
    "מהירות": None,
    "עוצמת אור": None,
    "ככלי": None,
    "מהירות סיבוב הלהב": None,
    "רוחב הקצעה": None,
    "עומק הקצעה": None,
    "סוללה": None,
    "כלי 1": None,
    "כלי 2": None,
    "מומנט פיטול": None,
    "פעימות לדקה": None,
    "סוג כלי:": None,
    "מתח העבודה:": None,
    "ויסות:": None,
    "מהירות סיבוב:": None,
    "סוג מנוע:": None,
    "מהלך חיתוך": None,
    "הטיית בסיס": None,
    "עובי חיתוך": None,
    "גיר": None,
    "קוטר צלחת": None,
    "מגנט לתלייה": None,
    "תפסן לתליה": None,
    "פיתול מרבי": None,
    "מצמד": None,
    "מוען מהיר": None,
    "קידוח מקסימלי": None,
    "קושר קידוח": None,
    "תפסן לחגורה": None,
    "כושר קידוח בעץ": None,
    "כושר קידוח בברזל": None,
    "כושר קידוח בבלוק": None,
    "שמן": None,
    "גודל מיכל": None,
    "לחץ": None,
    "ספיקה": None,
    "אורך": None,
    "עומק": None,
    "גובה": None,
    "עומס": None,
    "קוטר גיזום": None,
    "אורך החוט": None,
    "אורך להב": None,
    "חיתוך מקסימלי": None,
    "שימון שרשרת אוטומטי": None,
    "מהירות שרשרת": None,
    "הספק": None,
    "קוטר ציר": None,
    "גובה חיתוך ב90° של השולחן העליון": None,
    "הטיה": None,
    "קוטר אום מקסימאלי": None,
    "צינור גמיש באורך מטר": None,
    "רצועת כתף לעבודה בתנועה": None,
    "תאורת LED": None,
    "קוטר אום": None,
    "דיוק": None,
    "טווח עבודה": None,
    "צבע הקרן": None,
    "מברגת אימפקט": None,
    "מקדחה רוטטת": None,
    "קיבולת": None,
    "ווסת מהירויות": None,
    "מהירות דחיפה": None,
    "כוח דחיפה": None,
    "פטישון": None,
    "קוטר מלטשת": None,
    "אורך חיתוך ב45°": None,
    "אורך חיתוך ב90°": None,
    "קוטר דיסק מרבי": None,
    "משיכה": None,
    "איזמל": None,
    "אורך להב גיזום": None,
    "מרווח בין השיניים": None,
    "גובה כיסוח": None,
    "מיכל איסוף": None,
    "רוחב כיסוח ": None,
    "גובה מקסימלי": None,
    "גובה במצב מקופל": None,
    "תפסנית": None,
    "קוטר כרסום": None,
    "עומק כרסום": None,
    "עמיד למים ואבק בתקן IP65.": None,
    "טווח טמפרטורה": None,
    "זרימת אויר": None,
    "עומק חיתוך מירבי": None
}  

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
        return bool(response.css('div[data-elementor-type="product"]'))

    def extract_product_details(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # Reset values in table_data for this product
        for key in self.table_data.keys():
            self.table_data[key] = None

        breadcrumbs_href = response.css(".woocommerce-breadcrumb a ::attr(href)").getall()
        breadcrumbs_text = response.css(".woocommerce-breadcrumb a ::text").getall()
        category_url = breadcrumbs_href[1] if len(breadcrumbs_href) >= 2 else ""
        category_name = breadcrumbs_text[1] if len(breadcrumbs_text) >= 2 else ""
        subcategory_url = breadcrumbs_href[2] if len(breadcrumbs_href) >= 3 else ""
        subcategory_name = breadcrumbs_text[2] if len(breadcrumbs_text) >= 3 else ""
        product_url = response.url
        product_name = response.css("h1.product_title ::text").get()
        product_SKU = response.xpath("//div[@class='elementor-widget-container']/text()").re_first(r'מק״ט:\s*(\S+)')
        product_price = response.css(".price .woocommerce-Price-amount.amount bdi ::text").getall()[1]
        product_img = response.css(".woocommerce-product-gallery__image ::attr(data-thumb)").getall()
        product_img = [self.clean_url(url) for url in product_img]
        product_img_names = [re.search(r'/([^/]+)$', url).group(1) for url in product_img if re.search(r'/([^/]+)$', url)]
        prosuct_short_description = response.css(".woocommerce-product-details__short-description p ::text").get()
        prosuct_short_description_html = self.clean_style_html(response.css(".woocommerce-product-details__short-description").get())
        prosuct_more_description = '\n'.join(response.css(".elementor-widget-woocommerce-product-content p ::text").getall())
        prosuct_more_description_html = self.clean_style_html(response.css(".elementor-widget-woocommerce-product-content .elementor-widget-container").get())
        table_rows = response.css("table.shop_attributes tr")

        if table_rows:
            for row in table_rows:
                key = row.css("th ::text").get()
                value = row.css("td ::text").get()
                if key:
                    if key not in self.table_data:
                        self.table_data[key] = None  # Add new key if not already present
                    self.table_data[key] = value.strip() if value else None

        product_details = {
            "category_url": category_url,
            "category_name": category_name,
            "subcategory_url": subcategory_url,
            "subcategory_name": subcategory_name,
            "product_url": product_url,
            "product_name": product_name,
            "product_SKU": product_SKU,
            "product_price": product_price,
            "product_img": '\n'.join(product_img),
            "product_img_names": '\n'.join(product_img_names),
            "prosuct_short_description": prosuct_short_description,
            "prosuct_short_description_html": prosuct_short_description_html,
            "prosuct_more_description": prosuct_more_description,
            "prosuct_more_description_html": prosuct_more_description_html,
        }

        product_details.update(self.table_data)

        return product_details

    def is_valid_url(self, url):
        return self.allowed_domains[0] in url and "mailto:" not in url and "#" not in url
    
    def clean_style_html(self, selected_element):

        if selected_element:
            # Regular expressions to remove 'style' and 'class' attributes
            selected_element = re.sub(r'\s*style="[^"]*"', '', selected_element)  # Remove 'style' attributes
            selected_element = re.sub(r'\s*class="[^"]*"', '', selected_element)  # Remove 'class' attributes
            selected_element = re.sub(r'\s*dir="[^"]*"', '', selected_element)  # Remove 'dir' attributes
            selected_element = re.sub(r'<iframe.*?>.*?</iframe>', '', selected_element, flags=re.DOTALL)


            return selected_element
        
    def closed(self, reason):
        # Called when the spider finishes scraping
        self.export_to_excel()

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

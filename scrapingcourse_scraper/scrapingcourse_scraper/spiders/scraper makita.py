import scrapy
import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from openpyxl import Workbook

class SitemapSpider(scrapy.Spider):
    name = "scraper5"
    allowed_domains = ["www.makita-tools.co.il"]
    start_urls = ["https://www.makita-tools.co.il/"]

    visited_urls = set()  # Store visited URLs to avoid duplicates

    scraped_data = [] # in json for spliting to excel sheets
    
    # for attributes table
    table_data = {
    'מתח עבודה': None,
    'הספק': None,
    'כושר חיתוך': None,
    'אורך מהלך': None,
    'מהירות אלקטרונית': None,
    'משקל': None,
    'מנוע': None,
    'החלפת מסוריות': None,
    'מידות המוצר': None,
    'מהירות': None,
    'מידות': None,
    'מהירות אלקטרונית:': None,
    'משקל:': None,
    'תאורה': None,
    'עוצמת הלימה': None,
    'הלימות לדקה': None,
    'פחמים': None,
    'תקן איזמלים': None,
    'מיכל שימון': None,
    'קצב הלימה': None,
    'פוטר': None,
    'מס’ הלימות לדקה': None,
    'קוטר דיסק': None,
    'מהירות ללא עומס': None,
    'כושר ניסור ב-90°': None,
    'כושר ניסור ב-45°': None,
    'כושר חיתוך מרבי בצינור פלדה': None,
    'קוטר ציר': None,
    'מידות (אורך x רוחב x גובה)': None,
    'סוג': None,
    'קוטר הלהב': None,
    'כושר חיתוך מרבי 90° בצינור': None,
    'כושר חיתוך מרבי 45° בצינור': None,
    'כושר חיתוך מרבי 45° בפרופיל': None,
    'כושר חיתוך מרבי 90° בפרופיל': None,
    'תנועות לדקה': None,
    'כושר חיתוך מרבי בעץ': None,
    'כושר חיתוך מרבי בצינור': None,
    'מזוודה': None,
    'מהירות סיבוב': None,
    'מומנט פיתול': None,
    'סוללות': None,
    'מטען': None,
    'מגיע עם': None,
    'זווית תקיפה': None,
    'זווית הטייה מקסימלית': None,
    'יכולת חיתוך בעץ (90°)': None,
    'יכולת חיתוך בפלדה (90°)': None,
    'הבירות': None,
    'זווית הטייה מרבית': None,
    'טווח שיפוע מרבי (שמאל)': None,
    'חיתוך מרבי בעץ (90°)': None,
    'חיתוך מרבי בפלדה (90°)': None,
    'מידות מוצר (אורך x רוחב x גובה)': None,
    'מספר תנועות לדקה (SPM)': None,
    'חיבור לשואב אבק': None,
    'סוג מנוע': None,
    'רטיטות לדקה': None,
    'כושר חיתוך מקסימלי ב-90°': None,
    'קוטר להב': None,
    'עומק חיתוך מרבי (90 מעלות)': None,
    'עומק חיתוך מרבי (45 מעלות)': None,
    'מהירות סיבוב ללא עומס': None,
    'הלימות': None,
    'קוטר להב:': None,
    'כושר חיתוך:': None,
    'מהירות:': None,
    'כושר חיתוך 90°': None,
    'כושר חיתוך מרבי 90°': None,
    'כושר חיתוך מרבי 45°': None,
    'כושר חיתוך מרבי 50°': None,
    'עומק חיתוך בזווית 90°': None,
    'עומק חיתוך בזווית 45°': None,
    'עומק חיתוך בזווית 50°': None,
    'טווח שיפוע (שמאל)': None,
    'קוטר ציר (התקנה)': None,
    'מסילה': None,
    'עומק חיתוך מרבי ב-90°': None,
    'עומק חיתוך מרבי ב-48°': None,
    'עומק חיתוך מרבי ב-45°': None,
    'טווח הטיה מרבי (שמאל)': None,
    'גודל חור (קוטר ציר)': None,
    'כבל': None,
    'מידות המוצר (אורך x רוחב x גובה)': None,
    'גוף בלבד': None,
    'דרגות מהירות': None,
    'אורך להב': None,
    'סוג סוללה': None,
    'רוחב סיכות': None,
    'אורך סיכות': None,
    'מטען מהיר': None,
    'רטיטות': None,
    'מומנט פיטול': None,
    'תקן': None,
    'מחדות': None,
    'כושר חיתוך שולחן עליון': None,
    'מידות שולחן': None,
    'גובה חיתוך מרבי (מעל לשולחן) בזווית 90°': None,
    'גובה חיתוך מרבי (מעל לשולחן) בזווית 45°': None,
    'טווח הטייה מרבי (שמאל)': None,
    'גודל השולחן': None,
    'קוטר סרט': None,
    'מהירות סרט': None,
    '90°': None,
    '45°': None,
    'גובה חיתוך מרבי (מעל השולחן) בזווית 90°': None,
    'גובה חיתוך מרבי (מעל השולחן) בזווית 45°': None,
    'טווח הטיה מרבי (שמאלה)': None,
    'קוטר ציר (קוטר בור)': None,
    'מהירות עבודה ללא עומס': None,
    'חיתוך ב- 90°': None,
    'חיתוך ב- 45° שמאל': None,
    'חיתוך ב- שיפוע ימין 45°': None,
    'טווח נטוי מרבי (שמאל)': None,
    'קוטר דיסק:': None,
    'עומק מקסימלי:': None,
    'קוטר חור מרכזי בלהב': None,
    'אורך חיתוך מרבי ב-0°': None,
    'אורך חיתוך מרבי ב-45°': None,
    'עובי להב': None,
    'טווח הטיה שמאלה': None,
    'טווח הטיה ימינה': None,
    'גרונג שמאלי מרבי': None,
    'גרונג ימני מרבי': None,
    'מנגנון החלקה': None,
    'קיבולת חיתוך ב-90°': None,
    'יכולת פנדל שמאל/ימין': None,
    'יכולת הטיה שמאל/ימין': None,
    'עצירות זווית פנדל קבועות': None,
    'עצירות זווית הטיה קבועות': None,
    'סימון לייזר': None,
    'וויסות מהירות אלקטרונית': None,
    'יכולת חיתוך': None,
    'קוטר קידוח מרבי': None,
    'ציר': None,
    'הינע': None,
    'מומנט פריצת אום': None,
    'מהירות שרשרת': None,
    'צעד שרשרת': None,
    'עובי שרשרת': None,
    'אורך מסילה': None,
    'כמות חוליות': None,
    'נפח מיכל שמן': None,
    'הספק מוצא מרבי': None,
    'נפח': None,
    'מיכל דלק': None,
    '2 מצבי עבודה': None,
    'קוטר קידוח מרבי בטון': None,
    'עצמת הלימה': None
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
        product_SKU = response.xpath("//div[@class='elementor-widget-container']/h2[contains(@class, 'elementor-heading-title')]/text()").re_first(r'מק״ט\s*(\S+)')
        product_price = response.css(".price .woocommerce-Price-amount.amount bdi ::text").get()
        if product_price:
            product_price = product_price.replace(u'\xa0', u'')
        product_img = response.css(".woocommerce-product-gallery__image > a ::attr(href)").getall()
        product_img_names = [re.search(r'/([^/]+)$', url).group(1) for url in product_img if re.search(r'/([^/]+)$', url)]
        prosuct_short_description = response.css(".woocommerce-product-details__short-description p ::text").get()
        prosuct_short_description_html = response.css(".woocommerce-product-details__short-description").get()
        if prosuct_short_description_html:
            prosuct_short_description_html = self.remove_unwanted_attributes(prosuct_short_description_html)
        prosuct_more_description = '\n'.join(response.css("#tab-description ::text").getall())
        prosuct_more_description_html = response.css("#tab-description ").get()
        if prosuct_more_description_html:
            prosuct_more_description_html = self.remove_unwanted_attributes(prosuct_more_description_html)
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

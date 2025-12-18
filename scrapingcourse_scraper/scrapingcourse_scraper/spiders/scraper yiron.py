import scrapy
import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from openpyxl import Workbook
from urllib.parse import unquote

class SitemapSpider(scrapy.Spider):
    name = "yiron"
    allowed_domains = ["yiron.co.il"]
    start_urls = ["https://yiron.co.il/"]

    visited_urls = set()  # Store visited URLs to avoid duplicates

    scraped_data = [] # in json for spliting to excel sheets
    
    # for attributes table
    table_data = {
    
}
    sku_dict = {'https://yiron.co.il/product/%d7%9b%d7%95%d7%95%d7%a8%d7%aa-4-%d7%aa%d7%90%d7%99%d7%9d-2-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-618/': '618', 'https://yiron.co.il/product/%d7%a1%d7%a4%d7%a8%d7%99%d7%94-%d7%a8%d7%97%d7%91%d7%94-611/': '611', 'https://yiron.co.il/product/%d7%a9%d7%95%d7%9c%d7%97%d7%9f-%d7%9e%d7%97%d7%a9%d7%91-%d7%a2%d7%9d-%d7%9e%d7%93%d7%a3-%d7%9c%d7%9e%d7%93%d7%a4%d7%a1%d7%aa-204/': '204', 'https://yiron.co.il/product/%d7%a9%d7%95%d7%9c%d7%97%d7%9f-%d7%9e%d7%97%d7%a9%d7%91-%d7%a4%d7%99%d7%a0%d7%aa%d7%99-%d7%a2%d7%9d-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-229/': '229', 'https://yiron.co.il/product/%d7%a1%d7%a4%d7%a8%d7%99%d7%94-%d7%a6%d7%a8%d7%94-610/': '610', 'https://yiron.co.il/product/%d7%a9%d7%95%d7%9c%d7%97%d7%9f-%d7%9e%d7%97%d7%a9%d7%91-%d7%a2%d7%9d-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-225/': '225', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-2-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-%d7%9e%d7%a8%d7%95%d7%91%d7%94-%d7%9e%d7%93%d7%a4%d7%99%d7%9d-703/': '703', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-2-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-%d7%9e%d7%93%d7%a4%d7%99%d7%9d-%d7%95%d7%aa%d7%9c%d7%99%d7%94-702/': '702', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-2-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-2-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-606/': '606', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-4-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-%d7%9c%d7%99%d7%a8%d7%95%d7%9f/': '384', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%a0%d7%a2%d7%9c%d7%99%d7%99%d7%9d-4-%d7%aa%d7%90%d7%99%d7%9d-126/': '126', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%a2%d7%9c%d7%99%d7%95%d7%9f-3-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-607e/': '607E', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%a2%d7%9c%d7%99%d7%95%d7%9f-2-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-702e/': '702E', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%a2%d7%9c%d7%99%d7%95%d7%9f-4-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-710/': '710', 'https://yiron.co.il/product/%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-%d7%a4%d7%a0%d7%99%d7%9e%d7%99%d7%95%d7%aa-%d7%9c%d7%90%d7%a8%d7%95%d7%9f-709-709m/': '709M', 'https://yiron.co.il/product/%d7%9e%d7%93%d7%a3-%d7%a7%d7%98%d7%9f-%d7%9c%d7%90%d7%a8%d7%95%d7%9f-702m/': '702M', 'https://yiron.co.il/product/%d7%9e%d7%93%d7%a3-%d7%92%d7%93%d7%95%d7%9c-%d7%9c%d7%90%d7%a8%d7%95%d7%9f-767/': '767', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%a0%d7%a2%d7%9c%d7%99%d7%99%d7%9d-3-%d7%aa%d7%90%d7%99%d7%9d-125/': '125', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-%d7%9e%d7%99%d7%a7%d7%a8%d7%95%d7%92%d7%9c-%d7%a7%d7%98%d7%a0%d7%94-404/': '404', 'https://yiron.co.il/product/%d7%9e%d7%96%d7%95%d7%95%d7%94-%d7%a0%d7%99%d7%99%d7%93-%d7%a8%d7%91-%d7%a9%d7%99%d7%9e%d7%95%d7%a9%d7%99/': '508a', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%a0%d7%99%d7%aa-%d7%9e%d7%99%d7%a0%d7%99-%d7%9c%d7%aa%d7%a0%d7%95%d7%a8-%d7%91%d7%99%d7%9c%d7%98-%d7%90%d7%99%d7%9f/': '506a', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-%d7%a9%d7%99%d7%a8%d7%95%d7%aa-%d7%a0%d7%99%d7%99%d7%93%d7%aa/': '502a', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%a0%d7%99%d7%aa-%d7%a0%d7%99%d7%99%d7%93%d7%aa-%d7%a8%d7%91-%d7%aa%d7%9b%d7%9c%d7%99%d7%aa%d7%99%d7%aa/': '500a', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-%d7%a2%d7%9e%d7%95%d7%a7%d7%95%d7%aa-%d7%9c%d7%90%d7%97%d7%a1%d7%95%d7%9f-%d7%a1%d7%99%d7%a8%d7%99%d7%9d/': '505a', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%9c%d7%aa%d7%a0%d7%95%d7%a8-%d7%91%d7%99%d7%9c%d7%98-%d7%90%d7%99%d7%9f-%d7%95%d7%9e%d7%99%d7%a7%d7%a8%d7%95%d7%92%d7%9c/': '521a', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%a0%d7%99%d7%aa-%d7%90%d7%97%d7%a1%d7%95%d7%9f-%d7%9c%d7%9b%d7%99%d7%a8%d7%99%d7%99%d7%9d/': '504sa', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%94-%d7%9e%d7%a9%d7%95%d7%9c%d7%91%d7%aa-%d7%aa%d7%a0%d7%95%d7%a8-%d7%9e%d7%99%d7%a7%d7%a8%d7%95-%d7%98%d7%95%d7%a1%d7%98%d7%a8/': '573a', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-%d7%a7%d7%95%d7%9e%d7%95%d7%aa%d7%99%d7%99%d7%9d-%d7%a0%d7%99%d7%99%d7%93%d7%aa-%d7%9c%d7%9e%d7%99%d7%a7%d7%a8%d7%95%d7%92%d7%9c/': '503a', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-%d7%9e%d7%98%d7%91%d7%97-%d7%91%d7%a1%d7%99%d7%a1%d7%99%d7%aa/': '504a', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-4-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-%d7%95%d7%90%d7%a8%d7%95%d7%9f-%d7%a2%d7%9c%d7%99%d7%95%d7%9f-4-%d7%93%d7%9c%d7%aa%d7%95%d7%aa/': '709-10', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-4-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-2-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa%d7%90%d7%a8%d7%95%d7%9f-%d7%a2%d7%9c%d7%99%d7%95%d7%9f-4-%d7%93%d7%9c%d7%aa%d7%95%d7%aa/': '707-710', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-3-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-2-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-%d7%90%d7%a8%d7%95%d7%9f-%d7%a2%d7%9c%d7%99%d7%95%d7%9f-3-%d7%93%d7%9c%d7%aa%d7%95%d7%aa/': '607-607E', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%94%d7%96%d7%96%d7%94-%d7%97%d7%93%d7%a9/': '714', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%94%d7%96%d7%96%d7%94-%d7%a2%d7%9d-%d7%90%d7%a8%d7%91%d7%a2-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa/': '713', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%a2%d7%9c%d7%99%d7%95%d7%9f-2-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-%d7%9c-602/': '602E', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-2-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-%d7%9e%d7%a9%d7%95%d7%9c%d7%91-%d7%aa%d7%9c%d7%99%d7%94/': '602', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-2-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-%d7%9e%d7%a9%d7%95%d7%9c%d7%91-%d7%aa%d7%9c%d7%99%d7%94-%d7%90%d7%a8%d7%95%d7%9f-%d7%a2%d7%9c%d7%99%d7%95%d7%9f/': '602-602E', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-2-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-%d7%a0%d7%a2%d7%9e%d7%99/': '385', 'https://yiron.co.il/product/%d7%93%d7%92%d7%9d-%d7%a9%d7%9c%d7%99%d7%95-%d7%9e%d7%a7%d7%98-382/': '382', 'https://yiron.co.il/product/%d7%93%d7%92%d7%9d-%d7%a2%d7%9c%d7%9e%d7%94-%d7%9e%d7%a7%d7%98-387/': '387', 'https://yiron.co.il/product/%d7%93%d7%92%d7%9d-%d7%99%d7%94%d7%9c-%d7%9e%d7%a7%d7%98-410/': '410', 'https://yiron.co.il/product/%d7%93%d7%92%d7%9d-%d7%9b%d7%9c%d7%99%d7%9c-%d7%9e%d7%a7%d7%98-409/': '409', 'https://yiron.co.il/product/%d7%93%d7%92%d7%9d-%d7%93%d7%95%d7%a8-%d7%9e%d7%a7%d7%98-712/': '712', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%a0%d7%99%d7%99%d7%93-%d7%92%d7%93%d7%95%d7%9c-%d7%9c%d7%9e%d7%98%d7%91%d7%97-%d7%9e%d7%a7%d7%98-4008a/': '4008a', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%a0%d7%99%d7%aa-%d7%a2%d7%9c%d7%99%d7%95%d7%a0%d7%94-%d7%9c%d7%aa%d7%9c%d7%99%d7%99%d7%94-%d7%a2%d7%9c-%d7%94%d7%a7%d7%99%d7%a8-577a/': '577a', 'https://yiron.co.il/product/%d7%90%d7%99-%d7%90%d7%97%d7%a1%d7%95%d7%9f-%d7%92%d7%93%d7%95%d7%9c-%d7%95%d7%a4%d7%99%d7%a0%d7%aa-%d7%90%d7%95%d7%9b%d7%9c-805a/': '805a-1', 'https://yiron.co.il/product/%d7%90%d7%99-%d7%90%d7%97%d7%a1%d7%95%d7%9f-%d7%9c%d7%9e%d7%98%d7%91%d7%97-%d7%95%d7%a4%d7%99%d7%a0%d7%aa-%d7%90%d7%95%d7%9b%d7%9c-804a/': '804a-1-1', 'https://yiron.co.il/product/%d7%90%d7%99-%d7%9e%d7%a9%d7%95%d7%9c%d7%91-%d7%9c%d7%9e%d7%98%d7%91%d7%97-%d7%9b%d7%95%d7%9c%d7%9c-%d7%a9%d7%95%d7%9c%d7%97%d7%9f-%d7%9e%d7%aa%d7%a7%d7%a4%d7%9c-801a/': '801a', 'https://yiron.co.il/product/%d7%90%d7%99-%d7%a2%d7%a0%d7%a7-%d7%9c%d7%9e%d7%98%d7%91%d7%97-%d7%9e%d7%a9%d7%95%d7%9c%d7%91-%d7%a9%d7%95%d7%9c%d7%97%d7%9f-%d7%9e%d7%aa%d7%a7%d7%a4%d7%9c-803a/': '803a-1', 'https://yiron.co.il/product/%d7%90%d7%99-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-%d7%a1%d7%98%d7%a0%d7%93%d7%a8%d7%98%d7%99-%d7%9c%d7%9e%d7%98%d7%91%d7%97-802a/': '802a', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%a0%d7%99%d7%aa-%d7%9c%d7%aa%d7%a0%d7%95%d7%a8-%d7%9e%d7%95%d7%92%d7%91%d7%94-%d7%9e%d7%a9%d7%95%d7%9c%d7%91-%d7%9e%d7%99%d7%a7%d7%a8%d7%95%d7%92%d7%9c-777-2a/': '777a-2', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%a0%d7%99%d7%aa-%d7%a9%d7%99%d7%a8%d7%95%d7%aa-%d7%9c%d7%9e%d7%9b%d7%95%d7%a0%d7%aa-%d7%9b%d7%91%d7%99%d7%a1%d7%94-%d7%a8%d7%95%d7%a0%d7%94-%d7%9e%d7%a7%d7%98-411/': '411', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%99%d7%a8%d7%93%d7%9f-%d7%9e%d7%a7%d7%98-608/': '608', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%99%d7%a8%d7%93%d7%9f/': '608-607E-2', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%91%d7%99%d7%9c%d7%98-%d7%90%d7%99%d7%9f-%d7%9b%d7%a4%d7%95%d7%9c-%d7%9c%d7%99%d7%90%d7%95%d7%a8/': '412', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%a0%d7%a2%d7%9c%d7%99%d7%99%d7%9d-5-%d7%9e%d7%93%d7%a4%d7%99%d7%9d-127/': '127', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%a0%d7%a2%d7%9c%d7%99%d7%99%d7%9d-2-%d7%aa%d7%90%d7%99%d7%9d-124/': '124', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-%d7%9c%d7%99%d7%9c%d7%94-%d7%90%d7%9c%d7%94-%d7%9e%d7%a7%d7%98-360/': '360', 'https://yiron.co.il/product/%d7%a9%d7%95%d7%9c%d7%97%d7%9f-%d7%a1%d7%98%d7%95%d7%93%d7%a0%d7%98-%d7%97%d7%93%d7%a9/': '208', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-3-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-361/': '361', 'https://yiron.co.il/product/%d7%a9%d7%95%d7%9c%d7%97%d7%9f-%d7%a2%d7%9d-%d7%a1%d7%a4%d7%a8%d7%99%d7%94-613/': '613', 'https://yiron.co.il/product/%d7%a1%d7%a4%d7%a8%d7%99%d7%94-%d7%a2%d7%9d-2-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-612/': '612', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-4-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-709/': '709', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%a0%d7%99%d7%aa-%d7%92%d7%93%d7%95%d7%9c%d7%94-%d7%9c%d7%90%d7%97%d7%a1%d7%95%d7%9f-%d7%a1%d7%99%d7%a8%d7%99%d7%9d/': '522a', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%93%d7%9c%d7%aa-%d7%90%d7%97%d7%aa-700/': '700', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%a0%d7%99%d7%aa-%d7%9c%d7%aa%d7%a0%d7%95%d7%a8-%d7%95%d7%9b%d7%99%d7%a8%d7%99%d7%99%d7%9d/': '773a', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-3-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-2-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-607/': '607', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-%d7%9e%d7%99%d7%a7%d7%a8%d7%95%d7%92%d7%9c-%d7%9e%d7%94%d7%95%d7%93%d7%a8%d7%aa-405/': '405', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-%d7%93%d7%9c%d7%aa-%d7%90%d7%97%d7%aa-2-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-701/': '701', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-%d7%98%d7%9c%d7%95%d7%99%d7%96%d7%99%d7%94-2-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-509/': '509', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-4-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-2-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-707/': '707', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%a0%d7%99%d7%aa-%d7%9e%d7%99%d7%a7%d7%a8%d7%95%d7%92%d7%9c-4-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-407/': '407', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%a0%d7%99%d7%aa-%d7%92%d7%93%d7%95%d7%9c%d7%94-%d7%9c%d7%aa%d7%a0%d7%95%d7%a8-%d7%95%d7%9e%d7%99%d7%a7%d7%a8%d7%95%d7%92%d7%9c/': '519a', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%a0%d7%99%d7%aa-%d7%9c%d7%aa%d7%a0%d7%95%d7%a8-%d7%91%d7%99%d7%9c%d7%98-%d7%90%d7%99%d7%9f-%d7%9e%d7%95%d7%92%d7%91%d7%94/': '777a', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%a0%d7%99%d7%aa-%d7%9e%d7%98%d7%91%d7%97-%d7%a0%d7%99%d7%99%d7%93%d7%aa/': '501a', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%a0%d7%99%d7%aa-%d7%9e%d7%99%d7%a7%d7%a8%d7%95%d7%92%d7%9c-5-%d7%93%d7%9c%d7%aa%d7%95%d7%aa/': '408', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-2-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-2-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-375/': '375', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-3-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-2-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-376/': '376', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-5-%d7%9e%d7%92%d7%99%d7%a8%d7%95%d7%aa-374/': '374', 'https://yiron.co.il/product/%d7%a9%d7%99%d7%93%d7%aa-2-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-%d7%95%d7%9e%d7%92%d7%99%d7%a8%d7%94-%d7%90%d7%99%d7%aa%d7%9e%d7%a8/': '386', 'https://yiron.co.il/product/%d7%a9%d7%95%d7%9c%d7%97%d7%9f-%d7%a1%d7%98%d7%95%d7%93%d7%a0%d7%98-209/': '209', 'https://yiron.co.il/product/%d7%90%d7%a8%d7%95%d7%9f-2-%d7%93%d7%9c%d7%aa%d7%95%d7%aa-%d7%9e%d7%93%d7%a4%d7%99%d7%9d-%d7%95%d7%aa%d7%9c%d7%99%d7%94-%d7%90%d7%a8%d7%95%d7%9f-%d7%a2%d7%9c%d7%99%d7%95%d7%9f-2-%d7%93%d7%9c%d7%aa/': '702-702E'}
 

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
        return bool(response.css('div[data-elementor-type="jet-woo-builder"]'))


    def extract_product_details(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # Reset values in table_data for this product
        for key in self.table_data.keys():
            self.table_data[key] = None

        breadcrumbs_href = response.css(".woocommerce-breadcrumb a ::attr(href)").getall()
        breadcrumbs_text = response.css(".woocommerce-breadcrumb a ::text").getall()
        category_url = breadcrumbs_href[1] if len(breadcrumbs_href) >= 2 else ""
        category_name = breadcrumbs_text[1] if len(breadcrumbs_text) >= 2 else ""
        category_url2 = breadcrumbs_href[2] if len(breadcrumbs_href) >= 3 else ""
        category_name2 = breadcrumbs_text[2] if len(breadcrumbs_text) >= 3 else ""
        category_url3 = breadcrumbs_href[3] if len(breadcrumbs_href) >= 4 else ""
        category_name3 = breadcrumbs_text[3] if len(breadcrumbs_text) >= 4 else ""
        product_url = response.url
        product_name = response.css("h1.product_title ::text").get()
        product_price = response.css(".elementor-widget-jet-single-price .price .woocommerce-Price-amount.amount bdi ::text").getall()[1]
        # if product_price:
        #     product_price = product_price.replace(u'\xa0', u'')
        product_img = response.css('.swiper-wrapper .jet-woo-product-gallery__image-item img ::attr(src)').getall()
        product_img_names = [re.search(r'/([^/]+)$', url).group(1) for url in product_img if re.search(r'/([^/]+)$', url)]
        attr = response.xpath("//div[@class='elementor-widget-container']/span[contains(@class, 'elementor-heading-title')]/text()")
        product_SKU = attr[0].re(r'מק"ט:\s*(\S+)')
        materials = attr[1].re(r'חומרים:\s*(.+)') if len(attr) > 1 else None
        delivery_cost = attr[2].re(r'עלות הובלה:\s*(.+)') if len(attr) > 2 else None
        delivery_and_assembly = None
        if not delivery_cost:
            delivery_and_assembly = attr[2].re(r':\s*(.+)') if len(attr) > 2 else None
        Assembly_cost = response.css('.ppom-option-label-price ::text').get()
        Assembly_cost = Assembly_cost.strip("[]+") if Assembly_cost else None
        colors = response.css('select[id^="pa"] option ::text').getall()[1:]
        Assembly_instructions = response.css('.jet-listing-dynamic-link__link ::attr(href)').get()
        description = ''.join(response.css('.jet-listing-dynamic-field__content .product ::text').getall())
        descriptionHTML = response.css('.jet-listing-dynamic-field__content .product').getall()
        if descriptionHTML:
            descriptionHTML = self.remove_unwanted_attributes(descriptionHTML[0])
        
        linked_products = response.css('.products.columns-3 li a.woocommerce-LoopProduct-link ::attr(href)').getall()
        related_skus = [
            self.sku_dict.get(url)
            for url in linked_products
            if self.sku_dict.get(url) is not None
        ]
    

        product_details = {
            "category_url": category_url,
            "category_name": category_name,
            "category_url2": category_url2,
            "category_name2": category_name2,
            "category_url3": category_url3,
            "category_name3": category_name3,
            "product_url": product_url,
            "product_name": product_name,
            "product_SKU": product_SKU,
            "product_price": product_price,
            "materials": materials,
            "delivery_cost": delivery_cost,
            "Assembly_cost": Assembly_cost,
            "delivery_and_assembly": delivery_and_assembly,
            "colors": '\n'.join(colors),
            "Assembly_instructions": Assembly_instructions,
            "product_img": '\n'.join(product_img),
            "product_img_names": '\n'.join(product_img_names),
            "description": description,
            "descriptionHTML": descriptionHTML,
            "related_skus": '\n'.join(related_skus),
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

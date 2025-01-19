import scrapy
from urllib.parse import urlparse, urlunparse
import re

class SitemapSpider(scrapy.Spider):
    name = "scraper6"
    allowed_domains = ["huntertools.co.il"]
    start_urls = ["https://www.huntertools.co.il/"]

    visited_urls = set()  # Store visited URLs to avoid duplicates

    table_data = {'נתוני הכלי': '', 'הספק': None, 'מתח עבודה': None, 'מהירות ללא עומס': None, 'משקל': '15.7 ק"ג', 'פרטים נוספים': '', 'הספק ממוצע': '1500W', 'מתח': '230V', 'סמיכות צבע מקסימלית': None, 'מידה': None, 'נפח מיכל': None, 'מתאים לליין סוללות': None, 'זמן טעינה מטען 3A/h (סוללת 1.5A/h)': None, 'זמן טעינה מטען 3A/h (סוללת 3A/h)': None, 'זמן טעינה מטען 6.5A/h (סוללת 1.5A/h)': None, 'זמן טעינה מטען 6.5A/h (סוללת 3A/h)': None, 'זמן טעינה מטען 6.5A/h (סוללת 5A/h)': None, 'מהירות ללא עומס(RPM)': None, 'קלאץ': None, 'בורר מצב': None, 'תפסנית': None, 'משקל(גוף בלבד)': None, 'Lumens': None, 'COB': None, 'סוללה': None, 'שעות הפעלה (סוללה טעונה במלואה)': None, 'סוללה נטענת': None, '': None, 'הספק תאורת לד': None, 'עוצמת תאורה מירבית': None, 'טווח טמפרטורת סביבה': None, 'מטען (מתח וזרם טעינה)': None, 'זרם התנעה למצבר': None, 'מספר התנעות רציפות': None, 'גודל פיזי': None, 'תקן עמידות': None, 'יציאות ושקעים': None, 'מהירות ללא עומס (n1)': None, 'מהירות ללא עומס (n2)': None, 'קוטר הברגה': None, 'קוטר מוט': None, 'קוטר מוט עירבול': None, 'קוטר מוט ערבוב': None, 'מעבר חופשי': None, 'גובה סניקה': None, 'עוצמת שאיבה': None, 'אורך כבל': None, 'זמן טעינה מטען 3A/h (סוללת 3A/h )': None, 'סל”ד | 2 מהירויות': None, "הגדרות קלאצ'": None, 'ראשים מתחלפים': None, 'מומנט מקסימלי': None, 'מנוע': None, 'אור עבודה': None, 'קוטר מעבר חופשי': None, 'קוטר יציאה': None, 'מאפיינים מיוחדים': None, 'קצב שאיבה': None, 'מהירות (ללא עומס)': None, 'זמן פעולה': None, 'קוטר חיתוך': None, 'קוטר כבל / אורך': None, 'לחץ קול': None, 'עוצמת קול': None, 'רעידות': None, 'משקל (כולל סוללה)': None, 'מהירות סיבוב': '5000 סל"ד', 'קוטר דיסק': None, 'חיתוך באלומיניום': None, 'חיתוך ברזל': None, 'חיתוך בעץ': None, 'מהירות': None, 'שיפוע מקסימלי': None, 'קוטר משורית': None, 'קוטר הציר': None, 'סל”ד': None, 'קצב דפיקה': None, 'ידית אחיזה': None, 'הכנסה ושליפת ביטים ביד אחת': None, 'אריזה': None, 'אחריות בסיסית': None, 'אחריות מורחבת': None, 'מגיע עם': None, 'ניתן לרכוש בנפרד': None, 'קוטר ראש ליטוש': None, 'תכונות': None, 'מרווחי פנדל': None, 'חיתוך בזוית': None, 'שחרור משורית מהיר': None, 'מהירות זרימת אוויר': None, 'בורר מהירויות': None, 'לחצן מהירות טורבו': None, 'זמן עבודה במהירות מינימלית': None, 'עוצמת רעש(Lpa)': None, 'קצב דחיפת אוויר': None, 'תאימות סוללה': None, 'מצבי מהירות': None, 'זמען עבודה (סוללה מלאה)': None, 'נפח זרימת אוויר': None, 'עוצמת רעש (Lpa)': None, 'מידות': None, 'מהירות סיבוב (ללא עומס)': None, 'קוטר ציר': None, 'תכולת מיכל': None, 'זרימה': None, 'לחץ עבודה נומינלי': None, 'זמן טעינה מטען 3A/h (סוללת 5A/h)': None, 'מתאים לכל סוגי הסוללות': None, 'ראש בוקסה': None, 'מקסימום כוח': None, 'זמן טעינה מטען מהיר 6.5A/h (סוללת 3A/h)': None, 'זמן טעינה מטען מהיר 6.5A/h (סוללת 5A/h)': None, 'פנס': None, 'מהירות ללא עומס(LOW)': None, 'מהירות ללא עומס(HIGH)': None, 'בורר מצבים': None, 'תפסנית אוטומטית': None, 'מטען': None, 'שעות הפעלה': None, 'מצב סוללה': None, 'RPM': None, 'BPM': None, 'כוח דפיקה': None, 'כניסת תפסנית': None, 'קידוח בבטון': None, 'קוטר חיתוך דיסק': None, 'קוטר חיתוך חוט': None, 'מהירות סרק': None, 'קיבולת מיכל לאיסוף גזם': None, 'גובה חיתוך': None, 'רמת עוצמת קול מירבית LWA': None, 'סוללות': None, 'עוצמת הארה': None, 'רמקול': None, 'תקני עמידות': None, 'קצב דפיקה(BPM)': None, 'מומנט פתיחה': None, 'מומנט סגירה': None, 'קוטר גלגל השחזה': None, 'מידת דיסק הליטוש': None, 'מרחק עבודה מקסימלי': None, 'קוטר להב': '"8 / 210 ממ', 'כושר חיתוך': '', 'שולחן- זוית הטייה': '90° עד 45°', 'משור זוית': '', 'מהירות סיבובית (ללא עומס)': None, 'מידות אבן השחזה': None, 'מידות סרט ליטוש': None, 'מהירות סרט ליטוש': None, 'עוצמת רעש': None, 'מהירות סיבוב של הדיסק ללא עומס': None, 'מהירות סיבוב של החגורה ללא עומס': None, 'קוטר פד הליטוש': None, 'מידות סרט הליטוש': None, 'אורך הכבל': None, 'קוטר להב המשור': None, 'עומק ניסור': None, 'גובה שולחן': None, 'עובי להב': None, 'כיון זווית': None, 'גודל להב': None, 'כולל להב וידיה': None, 'חיתוך': None, 'כושר חיתוך ב- 90°': None, 'כושר חיתוך ב- 45°': None, 'מהירות להב': None, 'אורך להב': None, 'רוחב להב': None, 'עומק ניסור בזווית 90°': None, 'חיתוך בברזל': None, 'חיתוך אלומיניום': None, 'טווח תנועה': None, 'המשחזת מגיעה ללא דיסק': None, 'קוטר דיסק הליטוש': None, 'קוטר צינור שאיבה': None, 'גודל ציר': None, 'עומק חיתוך 90°': None, 'עומק חיתוך 45°': None, 'בעל תאורת לייזר': None, 'אורך להב הגוזם': None, 'מרווח בין שיניי המשור (יכולת גיזום)': None, 'מהירות הלהבים ללא עומס': None, 'רמץ לחץ הקול (Lpa)': None, 'רמת עוצמת הקול (Lwa)': None, 'רמת ויברציות לפי ידית': None, 'רמת בטיחות': None, 'מידות הכלי': None, 'משקל(כולל סוללה)': None, 'טווח טמפרטורה': None, 'טווח טמפרטורה מצב "|"': None, 'טווח טמפרטורה מצב "||"': None, 'כבל': None, 'צג': None, 'קוטר ניטים': None, 'משקל (ללא סוללה)': None, 'מתח הזנה/תדר': None, 'אורך להב השרשרת': None, 'מהירות השרשרת': None, 'נפח מיכל שימון שרשרת': None, 'קיבול מיכל שמן': None, 'לחץ עבודה': None, 'לחץ מקסימלי': None, 'קצב זרימת עבודה': None, "מקס' קצב זרימה": None, "מקס' אספקת מים בלחץ": None, 'LWA (כוח אקוסטי)': None, 'ערך רטט': None, "מקס' טמפרטורת מים": None, 'הגנת המכשיר מפני חדירת נוזלים': None, 'אחריות': None, 'יכולת קירור': None, 'יכולת חימום': None, 'זרם צריכה DC': None, 'איבוד חום לאחר ניתוק מהחשמל': None, 'קוטר מקסימלי': None, 'חור הרכבה': None, 'עומק ערוץ': None, 'רוחב ערוץ': None, 'מתח אספקה': None, 'צריכת הספק': None, 'גובה חיתוך (מתכוונן)': None, 'עוצמת קול מירבית LWA': None, 'להב חיתוך': None, 'טיפים של אלופים': None, 'קוטר קידוח מקסימלי': None, 'משקל (ללא מקדח)': None, 'מהירות ללא עומס (2 מהירויות, בסל"ד)': None, 'מידות הכלי (אורךXרוחבXגובה)': None, 'זמן עבודה': None, 'עומק הברשה': None, 'מידות (מצב פתוח)': None, 'מידות (מצב מקופל)': None, 'אורך כבל חשמל': None, 'קיבולת מיכל איסוף': None, 'רוחב מברשת': None, 'כושר קידוח לבנים': None, 'כושר קידוח בטון': None, 'מהירות ללא עומס 1 (סל"ד)': None, 'מהירות ללא עומס 2 (סל"ד)': None, 'סוג סוללה': None, 'כוח חיתוך מירבי': None, 'קוטר חיתוך ענפים מירבי': None, 'מימדים': None, 'מערכות בטיחות': None, 'קוטר כבל': None, 'הספק מנוע': None, 'מרווח שיניים': None, 'מתפס הלהב': None, 'הטיית ידית אחיזה': None, 'מערכת בטיחותית': None, 'אביזר גוזם גדר חי': None, 'אורך חיתוך': None, 'משקל(ללא אביזרים)': None, 'משקל כולל אביזר גוזם גדר': None, 'לחץ קול(LPA)': None, 'עוצמת קול(LWA)': None, 'מקסימום אורך מוט טלסקופי': None, 'אביזר משור שרשרת': None, 'מהירות משור ללא עומס': None, 'קיבולת מיכל שמן': None, 'משקל כולל אביזר משור שרשרת': None, 'נפח מנוע': None, 'נפח מיכל דלק': None, 'נפח מיכל שמן': None, 'רוחב חיתוך': None, 'עובי להבים': None, 'נפח שק איסוף': None, 'משקל נטו': None, 'עוצמת רעש LpA': None, 'ויברציות': None, 'גובה קיצוץ (6 מצבים)': None, 'קוטר צילינדר': None, 'דלק': None, 'דרך הצתה': None, 'מצת': None, 'התנעה': None, 'נפח מיכל דלק/שמן': None, 'משקל נקי': None, 'משקל ברוטו': None, 'מהירות במצב (ללא פעילות)': None, 'וע': None, 'להב': None, 'שרשרת': None, 'רעידות - ידית קדמית': None, 'רעידות - ידית אחורית': None, 'מהירות שרשרת': None, 'עומק חיתוך': None, 'מיכל שמן': None, 'קוטר המקדח (חורים)': None, 'מקדח 1': None, 'מקדח 2': None, 'מקדח 3': None, 'מהירות מירבית': None, 'סוג הצתה': None, 'אחוז שמן דלק': None, 'קיבולת מיכל דלק + שמן': None, 'כוח עבודה': None, 'קוטר': None, 'כושר': None, 'מלבן': None, 'מרובע': None, 'זוית הטייה (של המלחציים)': None, 'אביזרים במארז': None, 'כבל הזנה': None, 'מרחק בין הידיות': None, 'גובה (כולל מוטות)': None, 'מהירות גיר מצב I': None, 'מהירות גיר מצב II': None, 'חיבור מוטות ערבול': None, 'משקל (כולל מוטות)': None, 'טווח סיבוב שולחן המשור': None, 'משור זוית הטייה': None, 'שואב שבבים': None, 'מהירות עבודה ללא עומס': None, 'סוג לייזר': None, 'אורך גל הלייזר': None, 'סוג הגנה': None, 'עוצמת לייזר': None, 'עומק חיתוך בפלדה': None, 'עומק חיתוך בעץ': None, 'עומק חיתוך באלומיניום': None, 'חיתוך בזווית': None, 'גובה': None, 'אורך': None, 'משטח עבודה מקסימלי': None, 'עומק עומס מקסימלי': None, 'גובה פתיחה של גלגלות': None, 'אורך מוט': None, 'רמת רעש': None, 'המהירות ללא עומד': None, 'מידות פנדל': None, 'זווית הטיה': None, 'מפוח אוויר פנימי': None, 'רמות מהירות': None, 'אורן מוט': None, 'מתח הסוללה': None, 'אורך מוט590': None, 'ציר': None, 'זרימת ריסוס מקסימלית': None, 'אורך צינור ריסוס': None, 'משקל (כולל צינור)': None, 'רוחב המעבר': None, 'גובה המעבר': None, 'מסור זווית הטיה': None, 'גודל שולחן': None, 'מידות להב': None, 'הספק מרבי': None, 'גודל השולחן': None, 'אורך להב המסור': None, 'גובה חיתוך מקסימלי': None, 'עומק עבודה': None, 'תנועת הרמה': None, 'זווית חיתוך': None, 'גיר': None, 'גודל משטח עבודה': None, 'גודל בסיס המקדחה': None, 'מהירויות (סל"ד)': None, 'הספק מקסימלי': None, 'מערכת הנעה': None, 'קיבולת בנזין': None, 'משך פעולה רציפה': None, 'שמן מנוע': None, 'קיבולת שמן מנוע': None, 'רמת רעש (מרחק 7 מטרים)': None, 'מידות (מ"מ)': None, 'משקל כולל': None, 'ממיר מייצב מתח (AVR)': None, "קלאצ'": None, 'מקסימום פלט': None, 'יציאת DC': None, 'יציאת AC': None, 'מידה כוללת בס"מ(L×W×H)': None, 'עומק חיתוך עץ': None, 'עומק חיתוך פלדה': None, 'זמן טעינה (עם סוללה 1.5A)': None, '2 מהירויות סיבוב(תיבת הילוכים פלנטרית)': None, 'רטט בקידוח מתכת (Uncertainty K = 1,5 m/s)': None, 'רטט במצב הברגה ללא קידוח (Uncertainty K = 1,5 m/s)': None, 'תואם סוללה': None, 'משקל (גוף)': None, 'הילוכים': None, 'מהירויות חליצה': None, 'תאורת עבודה': None, 'משקל (גוף בלבד)': None, 'נפח מיכל הדלק': None, 'עומק חיתוך מקסימלי': None, 'מהירות במצב סיבובי סרק': None, 'קוטר דיסק הלהב': None, 'קוטר ציר הלהב': None, 'כוח סגירה של גלגל ההידוק': None, 'עוצמת רעד': None, 'משקל (ללא להב ודלק)': None, 'וואט': None, 'זרם': None, 'כושר הרמת כבל יחיד': None, 'כושר הרמת כבל כפול': None, 'גובה הרמה כבל יחיד': None, 'גובה הרמה כבל כפול': None, 'סל"ד כבל יחיד': None, 'סל"ד כבל כפול': None, 'עובי כבל': None, 'חוזק מתיחה של הכבל(N/mm)': None, 'רמת בידוד': None, 'רמת הגנה': None, 'סוג בידוד': None, 'מצב הפעלה': None, 'מנגנון מכני': None, 'דלק לתערובת (לא כלול)': None, 'שמן לתערובת (לא כלול)': None, 'יחס שמן דלק לשימוש': None, 'קרבורטור': None, 'קוטר ריסוק': None, 'מהירות משיכה': None, 'כוח משיכה': None, 'אורך כבל השחלה': None, 'קוטר כבל ההשחלה': None, 'עוצמת': None, 'קיבולת': None, 'אופציית': None, 'זרימת': None, 'מספר': None, 'מייצב מתח': None, 'מצבר': None, 'מומנט': None, '1': None, '2': None, '3': None, 'סיבובים לדקה (סל"ד)': None, 'ייצוב מתח': None, 'יציאות AC': None, 'פיה': None, 'תפסנית (אוטומטית)': None, 'קידוח במתכת': None, 'אביזרים': None, 'פוטר מיני למשחזת ציר': None, '5 דיסקיות לחיתוך מתכת': None, '70 יחידות נייר עגול לליטוש': None, '9 מכרסמים': None, '4 גלילי ליטוש גדולים': None, '4 גלילי ליטוש קטנים': None, '2 אביזרי שיוף בגדלים שונים': None, '7 אביזרי אבן להשחזה': None, '6 מברשות פלדה': None, 'משחת פוליש': None, 'אבן השחזה מלבנית': None, 'לחץ דחיסה': None, 'מתח חשמלי': None, 'הספק תאורת לד סה"כ': None, '2 תאורות צד מתקפלות': None, 'תאורה ראשית': None, 'זמני עבודה': None, 'כוח אקוסטי(LWA)': None, 'מידות הכלי(ס"מ)': None, 'תדר': None, 'הספק כניסה': None, 'מתח מקסימלי ללא עומס': None, 'עומס ללא עבודה': None, 'קבוצת בידוד': None, 'מתאים לריתוך אלקטרודות בטווח': None, 'קירור': None, 'מידות(HxLxW)': None, 'מהירות החוט': None, 'מחזור עבודה': None, 'קוטר חוט': None, "זרם מקס'": None, 'משקל (נטו)': None, 'לחץ שאיבה/יניקה': None, 'ספיקת אוויר': None, 'רמת שאיבה': None, 'אופציית שאיבה': None, 'מיכל': None, 'עוצמת מנוע': None, 'סל"ד מנוע': None, 'לחץ אוויר': None, 'יכולת דחיסה': None, 'כ"ס': None, 'קוטר מיכל': None, 'עומק הקצאה': None, 'עומק שיקוע': None, 'רוחב הקצעה (מקסימום)': None, 'אורך הלהב': None, 'עומק חיתוך ברזל': None, 'עומק חיתוך אלומיניום': None, 'תאימות עבודה': None, 'קליבה אינטגרלית': None, 'תאורת לייזר': None}

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
        return bool(response.css(".shop.productInfo"))

    def extract_product_details(self, response):

        # Reset values in table_data for this product
        for key in self.table_data.keys():
            self.table_data[key] = None

        breadcrumbs_href = response.css(".breadcrumb  a ::attr(href)").getall()
        breadcrumbs_href = ["https://www.huntertools.co.il" + href for href in breadcrumbs_href]
        breadcrumbs_text = response.css(".breadcrumb  a ::text").getall()
        category_url = breadcrumbs_href[2] if len(breadcrumbs_href) >= 3 else ""
        category_name = breadcrumbs_text[2] if len(breadcrumbs_text) >= 3 else ""
        category_url2 = breadcrumbs_href[3] if len(breadcrumbs_href) >= 4 else ""
        category_name2 = breadcrumbs_text[3] if len(breadcrumbs_text) >= 4 else ""
        category_url3 = breadcrumbs_href[4] if len(breadcrumbs_href) >= 5 else ""
        category_name3 = breadcrumbs_text[4] if len(breadcrumbs_text) >= 5 else ""
        category_url4 = breadcrumbs_href[5] if len(breadcrumbs_href) >= 6 else ""
        category_name4 = breadcrumbs_text[5] if len(breadcrumbs_text) >= 6 else ""
        product_url = response.url
        product_name = response.css(".productOrVariationTitle::text").get()
        product_SKU = response.css(".productSku ::text").get()   
        if product_SKU:
            product_SKU = product_SKU.replace('מק"ט: ', '').strip() 

        product_imgs = response.css(".swiper-slide.productImage ::attr(data-src)").getall()    
        product_img_names = [re.search(r'/([^/]+)$', url).group(1) for url in product_imgs if re.search(r'/([^/]+)$', url)]
        description = response.css(".productOrVariationSpoiler .collapse ::text").getall()
        description_html = response.css(".productOrVariationSpoiler .collapse").get()
        if description_html:
            description_html = self.remove_unwanted_attributes(description_html)
        
        table_rows = response.css("#tab2 table tr")

        if table_rows:
            extract_data = False  # A flag to track whether we are in the desired range

            # Iterate through the rows in the table
            for row in table_rows:
                header_text = row.css("td h3 ::text").get()  # Get the header text of the row

                # Check for the start of the desired range ("נתוני הכלי:")
                if header_text and "נתוני הכלי:" in header_text:
                    extract_data = True

                # If we're in the desired range, extract key-value pairs
                if extract_data:
                    # Get all <td> elements in the row
                    td_elements = row.css("td")
                    
                    # Ensure there are at least two <td> elements to extract a key-value pair
                    if len(td_elements) > 1:
                        key = td_elements[0].css("strong ::text").get() or td_elements[0].css("::text").get()  # Get key from the first <td>
                        value = td_elements[1].css("::text").get()  # Get value from the second <td>

                        if key and value:
                            # Replace '\xa0' with an empty string for both key and value
                            key = key.replace("\xa0", "").replace(":", "").strip()  # Clean up the key text and remove '\xa0'
                            value = value.replace("\xa0", "").replace(":", "").strip() if value else None  # Clean up the value text and remove '\xa0'

                            if key not in self.table_data:
                                self.table_data[key] = None  # Add new key if not already present
                            self.table_data[key] = value  # Add key-value pair to dictionary

                # Check for the end of the desired range ("פרטים נוספים:")
                if header_text and "פרטים נוספים:" in header_text:
                    extract_data = False


        product_details = {
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
            "product_img": self.extract_product_images(product_imgs),
            "product_img_names": product_img_names,
            "description": description,
            "description_html": description_html
        }

        product_details.update(self.table_data)

        return product_details
    

    def extract_product_images(self, product_imgs):
        # Join the image URLs into a single string, each separated by a newline
        return "https://www.huntertools.co.il" + "\nhttps://www.huntertools.co.il".join(product_imgs) if product_imgs else ""
    
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
        print(self.table_data)

    def is_valid_url(self, url):
        return self.allowed_domains[0] in url and "mailto:" not in url and "#" not in url
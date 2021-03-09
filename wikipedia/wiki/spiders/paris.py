import scrapy

class ParisSpider(scrapy.Spider):
    name = "paris"
    start_urls = ["https://www.keshart.in/work"]

    def parse(self, response):
        raw_image_url = response.css('img.gallery-item-visible.gallery-item.gallery-item-preloaded::attr(src)').getall()
        clean_image_url = []
        for img_url in raw_image_url:
            clean_image_url.append(response.urljoin(img_url))

        yield{
            'image_urls': clean_image_url
        }

import scrapy
from scrapy import Request
from practice2.items import Practice2Item
from scrapy.loader import ItemLoader

class StackOverflow(scrapy.Spider):
    name = "stack"
    start_urls = [f"https://stackoverflow.com/questions/tagged/python?tab=active&page={i}&pagesize=50" for i in range(1, 100)]

    def parse(self, response):
        questions = response.css("h3 a.question-hyperlink::attr(href)").extract()
        
        for ques in questions:
            yield Request(
                response.urljoin(ques),
                callback=self.parse_question,
            )
        next_page = response.xpath("//a[contains(text(), 'Next')]/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_question(self, response):
        l = ItemLoader(item=Practice2Item(), selector=response)
        l.add_css('ques', 'a.question-hyperlink')
        l.add_css('answer_by', 'div.user-details a')
        # l.add_css('answer', 'div.answer div.s-prose')
        # item['ques'] = response.css("a.question-hyperlink::text").get()
        yield l.load_item()
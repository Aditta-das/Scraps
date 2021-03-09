import scrapy
from scrapy import Request

class ScrapFilm(scrapy.Spider):
    name = "film"
    start_urls = ["https://yts.mx/browse-movies"]

    def parse(self, response):
        for f_s in response.css('.browse-movie-link::attr(href)').extract():
            yield Request (
                response.urljoin(f_s),
                callback=self.parse_movie_item,
            )
        next_page = response.xpath('//a[contains(text(), "Next")]/@href').extract_first()
        # print(next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_movie_item(self, response):
        details = response.css("#movie-info")
        name = details.css('h1::text').get()
        year = details.css('h2::text').get()
        imdb_rating = details.xpath('//span[@itemprop="ratingValue"]/text()').get()
        movie_poster = details.css('#movie-poster img::attr(src)').get()
        genres = details.css('div.hidden-xs h2::text').extract()[1].replace('/', ',')
        directors = details.xpath('//span[@itemprop="name"]/text()').get()
        item = {
            'name': name,
            'year': year,
            'imdb_rating': imdb_rating,
            'movie_poster': movie_poster,
            'genres': genres,
            'directors': directors,
            'cast': [],
            'similar_movies': []
        }
        cast = response.css('.actors .list-cast')
        for j, c in enumerate(cast):
            cast_name = c.css("span[itemprop='name']::text").extract()
            item['cast'].append({
                f'Cast_{j}': cast_name
            })
        
        movies_similar = response.css("#movie-related a::attr(title)").extract()
        for i, simi in enumerate(movies_similar):
            item['similar_movies'].append({
                f'Movie_{i}': simi
            })
        return item
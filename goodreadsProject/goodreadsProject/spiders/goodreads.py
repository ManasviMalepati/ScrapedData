import scrapy


class GoodreadsSpider(scrapy.Spider):
    name = 'goodreads'
    start_urls = ['https://www.goodreads.com/choiceawards/best-books-2020?ref=nav_brws_gca/']

    def parse(self, response):
        page_links = response.xpath("//div[@class='category clearFix']/a")
        yield from response.follow_all(page_links, self.parse_books)

        for genre in response.css('h4.category__copy::text'):
            yield {
                'genre': genre.get()
            }
        for link in response.xpath("//div[@class='category clearFix']/a"):
            yield{
                'link': link.get()
            }
    def parse_books(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'pageName': extract_with_css('title::text'),
            'bookTitle': extract_with_css('a.gcaBookTitle::text')
        }
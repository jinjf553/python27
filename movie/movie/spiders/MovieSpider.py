#^*^coding:utf-8^*^
#^*^user:jinjf553^*^
#^*^Email:jinjf553@gmail.com^*^
from scrapy.selector import Selector
from movie.items import MovieItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule


class MovieSpider(CrawlSpider):
    name = 'movie'
    download_delay = 1
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    rules = (
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/top250?start=\d',))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/top250?start=\d+',)), callback='parse_content'),
    )

    def parse(self, response):
        item = MovieItem()
        selector = Selector(response)
        movie = selector.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for each in movie:
            item['title'] = each.xpath('div/div[2]/div[1]/a/span[1]/text()').extract()[0]
            print(item['title'])
            content = each.xpath('div/div[2]/div[2]/p[1]/text()').extract()[0]\
                        +each.xpath('div/div[2]/div[2]/p[1]/text()[2]').extract()[0]
            item['movie_info'] = content.replace('\n','').replace(' ', '')
            item['star'] = each.xpath('div/div[2]/div[2]/div/span[2]/text()').extract()[0]
            item['quote'] = each.xpath('div/div[2]/div[2]/p[2]/span/text()').extract()[0]
            yield item
import scrapy

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['news.ycombinator.com']
    start_urls = ['https://news.ycombinator.com/news']

    def parse(self, response):
        job_title = response.xpath('//*[@class="storylink"]/text()').extract()
        job_link = response.xpath('//*[@class="storylink"]/@href').extract()
        job_points = response.xpath('//*[@class="score"]/text()').extract()

        for title, link, points in zip(job_title, job_link, job_points):
            yield {
                "Job Title": title,
                "Source URL": link,
                "Votes": points
            }

        next_page = response.xpath('//*[@class="morelink"]/@href').extract_first()
        next_page = response.urljoin(next_page)
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

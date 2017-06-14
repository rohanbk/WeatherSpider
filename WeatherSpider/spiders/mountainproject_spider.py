import scrapy


class MountainProjectSpider(scrapy.Spider):
    name = "mountainproject"

    def start_requests(self):
        urls = [
            # Massive test-case
            # 'https://www.mountainproject.com/',
            # Small sized test-case
            # 'https://www.mountainproject.com/v/kansas/107235316',
            # X-small sized test-case
            'https://www.mountainproject.com/v/hawaii-big-island/109264557'
        ]
        for url in urls:
            # yield scrapy.Request(url=url, callback=self.parse)
            yield scrapy.Request(url=url, callback=self.parse_region)

    def parse(self, response):
        for link in response.css('span.destArea'):

            # Extract regions on the MP homepage (e.g. States in the US, international, etc.).
            region = link.css('a::attr(href)').extract_first()
            if region is not None:
                region = response.urljoin(region)
                yield response.follow(region, callback=self.parse_region)

    def parse_region(self, region_response):
        # Gets all major area links within state
        # e.g. Washington > Central Region
        region_urls = region_response.css('div#viewerLeftNavColContent a[target="_top"]')
        if len(region_urls)==0:
            # TODO figure out how to store this to text file or append to JSON object
            yield {
                'title': region_response.css('#viewerLeftNavColContent b::text').extract_first(),

                # TODO figure out how to convert $('div#rspCol800 div.rspCol table tr:eq(1) td:eq(1)').text() into CSS/XPATH selector
                'latitude' : '',
                'longitude' : '',
                 'breadCrumbTrail' : ''
            }

        for link in region_urls:
            area = link.css('a::attr(href)').extract_first()
            if area is not None:
                yield region_response.follow(region_response.urljoin(area), callback=self.parse_region)


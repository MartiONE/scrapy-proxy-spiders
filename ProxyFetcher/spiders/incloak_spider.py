import scrapy
from ProxyFetcher.items import ProxyfetcherItem

class InCloakSpider(scrapy.Spider):
    
        name = "incloak"
        allowed_domains = ["incloak.com"]
        start_urls = [
            "http://incloak.com/proxy-list/?maxtime=1000&type=hs#list"
        ]    
        
        def parse(self, response):
                for page in response.xpath("//div[@class='proxy__pagination']/ul/li[not(@class) or @class='is-active']/a/@href"):
                        print(page)
                        url = response.urljoin(page.extract())
                        yield scrapy.Request(url, callback=self.parse_page)
        def parse_page(self, response):
                for row in response.xpath("//table[@class='proxy__t']/tbody/tr"):
                        item = ProxyfetcherItem()
                        item["ip"] = row.xpath("td[1]/text()").extract()[0].strip()
                        item["port"] = row.xpath("td[2]/text()").extract()[0].strip()
                        item["country"] = row.xpath("td[3]/div/text()").extract()[0].strip()
                        # Split for the dual mode, getting only http
                        item["con_type"] = row.xpath("td[5]/text()").extract()[0].split(", ")[0]
                        item["full_address"] = "{}:{}".format(item["ip"], item["port"])
                        yield item.status_check(item)

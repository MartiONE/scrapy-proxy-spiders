import scrapy
from ProxyFetcher.items import ProxyfetcherItem

class SSLproxies(scrapy.Spider):
    
        name = "sslproxies"
        allowed_domains = ["https://www.sslproxies.org/"]
        start_urls = [
            "https://www.sslproxies.org/"
        ]    
        
        def parse(self, response):
                for j in response.xpath("//tbody/tr"):
                        # Item creation and deployment
                        item = ProxyfetcherItem()                        
                        item["ip"] = j.xpath("td[1]/text()").extract()[0].strip()
                        item["port"] = j.xpath("td[2]/text()").extract()[0].strip()
                        item["country"] = j.xpath("td[4]/text()").extract()[0].strip()
                        item["con_type"] = "https"
                        item["full_address"] = "{}:{}".format(item["ip"], item["port"])
                        yield item.status_check(item)

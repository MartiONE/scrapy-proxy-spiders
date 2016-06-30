import scrapy
from ProxyFetcher.items import ProxyfetcherItem

class FreeProxyListNet(scrapy.Spider):
    
        name = "freeproxylistnet"
        allowed_domains = ["http://free-proxy-list.net/"]
        start_urls = [
            "http://free-proxy-list.net/"
        ]    
        
        def parse(self, response):
                for j in response.xpath("//table[@id='proxylisttable']/tbody/tr"):
                        # Item creation and deployment
                        item = ProxyfetcherItem()                        
                        item["ip"] = j.xpath("td[1]/text()").extract()[0].strip()
                        item["port"] = j.xpath("td[2]/text()").extract()[0].strip()
                        item["country"] = j.xpath("td[4]/text()").extract()[0].strip()
                        item["con_type"] == "http" if j.xpath("td[7]/text()").extract()[0].strip() == "no" else "https"
                        item["full_address"] = "{}:{}".format(item["ip"], item["port"])
                        yield item.status_check(item)
                        
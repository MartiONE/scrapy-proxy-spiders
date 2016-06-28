import scrapy
from ProxyFetcher.items import ProxyfetcherItem
import base64

class ProxyListSpider(scrapy.Spider):
    
        name = "proxylist"
        allowed_domains = ["proxy-list.org"]
        start_urls = [
            "https://proxy-list.org/english/index.php"
        ]    
        
        def parse(self, response):
                for j in response.xpath("//div[@class='table']/ul"):
                        # Item creation and deployment
                        item = ProxyfetcherItem()
                        # This website use a base64 encoding as payload for a js function
                        item["full_address"] = base64.b64decode(j.xpath("li[@class='proxy']/script/text()")[0].re("Proxy\(\'(.+)\'")[0]).decode("utf-8")
                        item["ip"], item["port"] = item["full_address"].split(":")
                        # Even http classes do not exists they might in the future, so better safe than sorry.-
                        item["con_type"] = j.xpath("li[@class='http' or @class='https']/text()").extract()[0].strip().lower()
                        item["country"] = j.xpath("descendant::span[@class='country']/@title").extract()[0].strip()
                        yield item.status_check(item)
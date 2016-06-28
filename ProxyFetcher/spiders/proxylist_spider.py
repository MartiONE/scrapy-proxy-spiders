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
                # Parse the footer page list
                for page in response.xpath("//div[@class='table-menu']/a[@class='item']/@href"):
                        # Relative url, need to.
                        url = response.urljoin(page.extract())
                        yield scrapy.Request(url, callback=self.parse_page)
        
        def parse_page(self, response):
                for j in response.xpath("//div[@class='table']/ul"):
                        # Item creation and deployment
                        item = ProxyfetcherItem()
                        # This website use a base64 encoding as payload for a js function
                        item["full_address"] = base64.b64decode(j.xpath("li[@class='proxy']/script/text()")[0].re("Proxy\(\'(.+)\'")[0]).decode("utf-8")
                        item["ip"], item["port"] = item["full_address"].split(":")
                        # Even http classes do not exists they might in the future, so better safe than sorry.-
                        item["con_type"] = j.xpath("li[@class='http' or @class='https']/text()|li/strong/text()").extract()[0].strip().lower()
                        # Replace used for the special use case of the &nbsp;
                        item["country"] = j.xpath("descendant::span[@class='country']/@title").extract()[0].strip().replace("\xa0", " ")
                        yield item.status_check(item)
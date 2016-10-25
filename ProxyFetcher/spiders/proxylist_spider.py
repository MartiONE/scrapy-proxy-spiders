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
                yield self.parse_page(response)
        
        def parse_page(self, response):
                for j in response.xpath("//div[@class='table']/ul"):
                        # Item creation and deployment
                        item = ProxyfetcherItem()
                        # This website use a base64 encoding as payload for a js function
                        item["full_address"] = str(base64.b64decode(j.xpath("li[@class='proxy']/script/text()")[0].re("Proxy\(\'(.+)\'")[0]).decode("utf-8"))
                        item["ip"], item["port"] = item["full_address"].split(":")
                        # Even http classes do not exists they might in the future, so better safe than sorry.-
                        ctype = j.xpath("li[@class='http' or @class='https']/text()|li/strong/text()").extract()[0].strip().lower()
                        item["con_type"] = "http" if ctype == "-" else ctype
                        # Replace used for the special use case of the &nbsp;
                        item["country"] = str(j.xpath("descendant::span[@class='country']/@title").extract()[0].strip().replace(u"\xa0", " "))
                        yield item.status_check(item)

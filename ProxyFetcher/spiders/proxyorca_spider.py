import scrapy
from ProxyFetcher.items import ProxyfetcherItem

# Spider for the forum of the website proxyorca.com

class ProxyOrcaSpider(scrapy.Spider):
    name = "proxyorca"
    allowed_domains = ["proxyorca.com"]
    start_urls = [
        "http://proxyorca.com/forum/forumdisplay.php?fid=4&page=1"
    ]
    
    def parse(self, response):
        for link in response.xpath("//tr[@class='inline_row']/td/div/span/span/a[1]/@href"):
            link = response.urljoin(link.extract())
            yield scrapy.Request(link, callback=self.parse_postresponse)
            
    def parse_postresponse(self, response):
        for proxy in response.xpath("//div[@class='post_body scaleimages']")[0].xpath("text()").extract()[1:-3]:
            # Trim and split the proxy
            proxy = proxy.replace("\n", "").split(":")
            
            item = ProxyfetcherItem()
            item["ip"] = proxy[0]
            item["port"] = proxy[1]
            item["con_type"] = "http"
            item["country"] = "NaN"
            
            yield item.status_check(item)
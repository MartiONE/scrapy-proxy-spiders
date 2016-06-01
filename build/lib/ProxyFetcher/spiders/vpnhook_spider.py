import scrapy
import requests
import time
import logging

from ProxyFetcher.items import ProxyfetcherItem


class VpnhookProxySpider(scrapy.Spider):
    name = "vpnhook"
    allowed_domains = ["vpnhook.com"]
    start_urls = [
        "http://vpnhook.com/proxysocks/"
    ]
    
    def parse(self, response):
        # Not-so-good xpath but working nontheless, upgradeable
        for r in response.xpath("/html/body/div[1]/div/section/article/div[2]/div/div/a/@href"):
            # Using response method to extract and parse the url just in case it is relative
            url = response.urljoin(r.extract())
            yield scrapy.Request(url, callback=self.parse_table_contents)
    
    def parse_table_contents(self, response):
        for proxy_info in response.xpath("//table[@id='proxytable']/tr"):
            # Iterate every item found
            if proxy_info.xpath("td"):
                item = ProxyfetcherItem()
                item["ip"] = proxy_info.xpath("td/text()")[0].extract().strip()
                item["port"] = proxy_info.xpath("td/text()")[1].extract().strip()
                item["country"] = proxy_info.xpath("td/text()")[2].extract().strip()
                item["con_type"] = proxy_info.xpath("td/text()")[3].extract().strip()
                
                yield item.status_check(item)
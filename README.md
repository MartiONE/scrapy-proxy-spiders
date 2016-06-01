# Description

Simple spiders made using Scrapy to retrieve free proxys from websited publishing them.
We use a simple judge to filter them.

# Requirements

- [Scrapy](http://scrapy.org/)
- [Requests](http://docs.python-requests.org/en/master/)

# Basic Usage

This will output via console the results of the spider of the website proxyorca.
```
scrapy crawl proxyorca
```

If we want to save the results into a file 

```
scrapy crawl proxyorca -o items.json
```


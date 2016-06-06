# Description

Simple spiders made using Scrapy to retrieve free proxys from websited publishing them.
We use a simple judge to filter them.

# Requirements

- [Scrapy](http://scrapy.org/)
- [Requests](http://docs.python-requests.org/en/master/)
- [SQLAlchemy](http://www.sqlalchemy.org/)


# Configuration

You'll need to configure the settings.py file using this template

    DATABASE = {'drivername': 'postgres',
              'host': 'Host',
              'port': '5432',
              'username': 'Your database username',
              'password': 'Password',
              'database': 'Database selected'}

# Basic Usage

This will output via console the results of the spider of the website proxyorca.
```
scrapy crawl proxyorca
```

If we want to save the results into a file 

```
scrapy crawl proxyorca -o items.json
```


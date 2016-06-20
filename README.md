# Description

Simple spiders made using Scrapy to retrieve free proxys from websited publishing them.
We use a simple judge to filter them.

# Requirements

- [Scrapy](http://scrapy.org/)
- [Requests](http://docs.python-requests.org/en/master/)
- [SQLAlchemy](http://www.sqlalchemy.org/)


# Configuration

You'll need to configure the general.cfg file using this template:

Postgres database where we will store the results.

    [postgres]
    drivername = postgres 
    host = >Postgres host<
    port = >5432 by default<
    username = >Postgres username<
    password = >Postgres passwd<
    database = >Postgres database name
              
Optionally we can also configure a redis database that will deliver the fresh proxies to our app:
    
    [remote_redis]
    host = >Redis host<
    port = >Redis port<
    password = >Redis passwd<
    
    
Also, if you want to run the job periodically, you can set up crontab to work with virtualenv.
WITH THE VIRTUALENV ACTIVATED

    $ echo "PATH=$PATH" > myserver.cron
    $ crontab -l >> myserver.cron
    $ crontab myserver.cron

Crontab file will now look like:

    PATH=/home/me/virtualenv/bin:/usr/bin:/bin:  # [etc...]
    
Then add the jobs like:
    
    1 * * * * sh ~/Your-project-folder/cronscripts/execute_spider.sh vpnhook >>/tmp/cron_debug_log.log 2>&1
    
Please note that the trailing addition is for log and debug purposes, and the execute spider is a generic script.

# Basic Usage

This will output via console the results of the spider of the website proxyorca.
```
scrapy crawl proxyorca
```

If we want to save the results into a file 

```
scrapy crawl proxyorca -o items.json
```


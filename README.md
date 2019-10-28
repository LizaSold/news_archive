# News_archive
News-database that is regularly updated

# What does it do
 - Crawl url: https://www.spiegel.de/international/
 - Extract News-Entries from HTML
    * Title
    * Sub-Title
    * Abstract
    * Download-time 
 -  Store these entries in a Postgresql database
 -  The crawler is triggered to run automatically every 15 minutes
 -  During re-runs, existing entries are detected and not stored as duplicates, but an additional timestamp is stored: update-time

News page example:
![example](https://sun9-61.userapi.com/c853428/v853428060/13502b/K22N4RGYelQ.jpg)

Database screenshot:
![database look](https://sun9-29.userapi.com/c853428/v853428960/131b65/hcetUa5gGI4.jpg)

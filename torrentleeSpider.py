import scrapy
import os
import sys
from urllib import quote, unquote
from datetime import datetime

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    def __init__(self,*args,**kwargs):
        super(BlogSpider, self).__init__(*args, **kwargs)
        self.domain = kwargs.get('domain')
        self.search = kwargs.get('search')
        self.seconds = int(kwargs.get('seconds'))
        self.path = kwargs.get('path')
        self.bo_table = kwargs.get('bo_table')
        url = self.domain + "/bbs/board.php?bo_table=" + self.bo_table + "&sca=&sop=and&sfl=wr_subject&stx=" + quote(self.search)
        print "BUILD " + url
        self.start_urls = [ url ]

#    start_urls = ['http://www.tosarang2.net/bbs/board.php?bo_table=torrent_kortv_drama&sca=&sop=and&sfl=wr_subject&stx=%ED%83%9C%EC%96%91%EC%9D%98+%ED%9B%84%EC%98%88']

    def parse(self, response):
        Urllist = response.css('td.td_subject > a::attr("href")')
        for url in Urllist.re(self.domain + "/bbs/board.php.*"):
#            print url
            yield scrapy.Request(response.urljoin(url), self.parse_contents)

    def parse_contents(self, response):
        title = response.css('div#contents > div#bo_v > div#bo_v_title > h1::text').extract()
        urlList = response.css('div#contents > div#bo_v > div.bo_v_file > a::attr("href")').re("magnet:.*&")
        createTime = response.css('div#contents > div#bo_v > div.bo_v_torrent > table > tr > td.value::text').re("[0-9]{4}-[0-9]{2}-[0-9]{2}.*")
        command = "transmission-remote 9091 -w " + self.path + " -a " + urlList[0]
        nowDateTime = datetime.now()
        createDateTime = datetime.strptime(createTime[0],'%Y-%m-%d %H:%M:%S')
        diffSeconds = ( nowDateTime - createDateTime ).total_seconds()
        if diffSeconds < self.seconds :
            print "INFO [torrent]torrent download start"
            print "INFO title : " + title[0].encode("utf-8").strip()
            print "\nINFO url : " + response.request.url.encode("utf-8")
            print "\nINFO command : " + command.encode("utf-8")
            print "\nINFO creatTime : " + createTime[0]
            print "\nINFO diff seconds : " + str(diffSeconds)
            os.system(command.encode('utf-8'))

        yield {"title" : title[0].encode("utf-8").strip(), "url" : response.request.url.encode("utf-8") , "command" : command.encode("utf-8"), "createTime" : createTime[0] , "seconds" : diffSeconds }

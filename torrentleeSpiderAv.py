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
        print "BUILDTORRENT " + url
        self.start_urls = [ url ]

#    start_urls = ['http://www.tosarang2.net/bbs/board.php?bo_table=torrent_kortv_drama&sca=&sop=and&sfl=wr_subject&stx=%ED%83%9C%EC%96%91%EC%9D%98+%ED%9B%84%EC%98%88']

    def parse(self, response):
        Urllist = response.css('li.li_subject > a::attr("href")')
        for url in Urllist.re(".*/bbs/board.php.*"):
            #print url
            yield scrapy.Request(response.urljoin(url), self.parse_contents)

    def parse_contents(self, response):
        title = response.css('header#bo_v_title > div > h3::text').extract()
        urlList = response.css('section#bo_v_link > ul.list-unstyled > li > div > div > a::attr("href")').re("magnet:.*&")
        createTime = response.css('section#bo_v_torrent > table > tr > td.value::text').re("[0-9]{4}-[0-9]{2}-[0-9]{2}.*")[0]
        command = "transmission-remote 9091 -w " + self.path + " -a " + urlList[0]
        nowDateTime = datetime.now()
        createDateTime = datetime.strptime(createTime,'%Y-%m-%d %H:%M:%S')
        diffSeconds = ( nowDateTime - createDateTime ).total_seconds()
        if diffSeconds < self.seconds :
            print "INFOTORRENT [torrent]torrent download start"
            print "INFOTORRENT title : " + title[0].encode("utf-8").strip()
            print "\nINFOTORRENT url : " + response.request.url.encode("utf-8")
            print "\nINFOTORRENT command : " + command.encode("utf-8")
            print "\nINFOTORRENT creatTime : " + createTime
            print "\nINFOTORRENT diff seconds : " + str(diffSeconds)
            os.system(command.encode('utf-8'))

        yield {"title" : title[0].encode("utf-8").strip(), "url" : response.request.url.encode("utf-8") , "command" : command.encode("utf-8"), "createTime" : createTime , "seconds" : diffSeconds }

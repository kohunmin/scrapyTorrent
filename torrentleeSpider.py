import scrapy
import os
import sys
from urllib import quote, unquote
from datetime import datetime

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    def __init__(self,*args,**kwargs):
        super(BlogSpider, self).__init__(*args, **kwargs)
        self.search = kwargs.get('search')
        self.seconds = kwargs.get('seconds')
        self.start_urls = ["http://www.tosarang2.net/bbs/board.php?bo_table=torrent_kortv_drama&sca=&sop=and&sfl=wr_subject&stx=" + quote(self.search)]

#    start_urls = ['http://www.tosarang2.net/bbs/board.php?bo_table=torrent_kortv_drama&sca=&sop=and&sfl=wr_subject&stx=%ED%83%9C%EC%96%91%EC%9D%98+%ED%9B%84%EC%98%88']

    def parse(self, response):
        Urllist = response.css('td.td_subject > a::attr("href")')
        for url in Urllist.re('http://www.tosarang2.net/bbs/board.php.*'):
#            print url
            yield scrapy.Request(response.urljoin(url), self.parse_contents)

    def parse_contents(self, response):
        urlList = response.css('div#contents > div#bo_v > div.bo_v_file > a::attr("href")').re("magnet:.*&")
        createTime = response.css('div#contents > div#bo_v > div.bo_v_torrent > table > tr > td.value::text').re("[0-9]{4}-[0-9]{2}-[0-9]{2}.*")
        command = "transmission-remote 9091 -a " + urlList[0]
        nowDateTime = datetime.now()
        createDateTime = datetime.strptime(createTime[0],'%Y-%m-%d %H:%M:%S')
        diffDateTime = nowDateTime - createDateTime
        if diffDateTime.seconds < self.seconds :
            print ( "url" , urlList[0] , "command", command, 'seconds', diffDateTime.seconds )
            os.system(command.encode('utf-8'))

        yield {'url' : urlList[0]}

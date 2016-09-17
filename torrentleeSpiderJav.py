import scrapy
import os
import sys
import time
import re
from urllib import quote, unquote
from datetime import datetime

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    def __init__(self,*args,**kwargs):
        super(BlogSpider, self).__init__(*args, **kwargs)
        self.downloadPath = kwargs.get('toDownPath')
        self.path = kwargs.get('path')
        self.search = kwargs.get('search')
        #self.search = "%E9%88%B4%E5%8E%9F%E3%82%A8%E3%83%9F%E3%83%AA";
        self.seconds = kwargs.get('sec')
        url = "http://javtorrent.xyz/tag/" + self.search + "/";
        print "BUILDTORRENT " + url
        self.start_urls = [ url ]

    def parse(self, response):
        nowDateTime = datetime.now()
        Urllist = response.css('div#content > div#archive-posts > div.posts-default > li > span.entry-dl > a::attr("href")')
        Datelist = response.css('div#content > div#archive-posts > div.posts-default > li > a.entry-thumbnails-link > span.cate-meta > span.cate-ti::text').extract()
	print len(Datelist)
	print len(Urllist)
        for idx , url in enumerate(Urllist.re(".*biz/j.php.*")):
            time.sleep(0.1)
            date = Datelist[idx]
            createDateTime = datetime.strptime(date,'%Y/%m/%d - %H:%M')
            diffSeconds = ( nowDateTime - createDateTime ).total_seconds()
            if int(diffSeconds) < int(self.seconds) :
                print "INFOTORRENT " + url
                yield scrapy.Request(url, self.contents1)

    def contents1(self, response):
        links = response.css('a::attr("href")').re(".*biz/d.php.*")
        for link in links:
            time.sleep(0.1)
            yield scrapy.Request(link, self.contents2)

    def contents2(self, response):
        downloadLink = response.css('a::attr("href")').re(".*torrent")[0]
        #print downloadLink
        time.sleep(0.1)
        downloadLinkArray = downloadLink.split('/')
        fileName = downloadLinkArray[len(downloadLinkArray) - 1]
        wgetCommand = "wget --referer=" + response.request.url + " " + downloadLink + " -P " + self.downloadPath
        transCallCommand = "transmission-remote 9091 -w " + self.path
        transCallCommand += " -a " + self.downloadPath + str(fileName)
        print "INFOTORRENT " + transCallCommand
        os.system(wgetCommand)
        os.system(transCallCommand)



#        title = response.css('div#contents > div#bo_v > div#bo_v_title > h1::text').extract()
#        urlList = response.css('div#contents > div#bo_v > div.bo_v_file > a::attr("href")').re("magnet:.*&")
#        hit = response.css('div#contents > div#bo_v > div.bo_v_info > td.td_info_right::text').re("[")
#        print hit
#        createTime = response.css('div#contents > div#bo_v > div.bo_v_torrent > table > tr > td.value::text').re("[0-9]{4}-[0-9]{2}-[0-9]{2}.*")
#        command = "transmission-remote 9091 -w " + self.path + " -a " + urlList[0]
#             print "INFOTORRENT [torrent]torrent download start"
            # print "INFOTORRENT title : " + title[0].encode("utf-8").strip()
            # print "\nINFOTORRENT url : " + response.request.url.encode("utf-8")
            # print "\nINFOTORRENT command : " + command.encode("utf-8")
            # print "\nINFOTORRENT creatTime : " + createTime[0]
            # print "\nINFOTORRENT diff seconds : " + str(diffSeconds)
            # os.system(command.encode('utf-8'))
        #
        # yield {"title" : title[0].encode("utf-8").strip(), "url" : response.request.url.encode("utf-8") , "command" : command.encode("utf-8"), "createTime" : createTime[0] , "seconds" : diffSeconds }

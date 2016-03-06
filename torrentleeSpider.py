import scrapy
import os
import sys

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://www.tosarang2.net/bbs/board.php?bo_table=torrent_kortv_drama&sca=&sop=and&sfl=wr_subject&stx=%ED%83%9C%EC%96%91%EC%9D%98+%ED%9B%84%EC%98%88']

    def parse(self, response):
        Urllist = response.css('td.td_subject > a::attr("href")')
        for url in Urllist.re('http://www.tosarang2.net/bbs/board.php.*'):
            print url
            yield scrapy.Request(response.urljoin(url), self.parse_contents)

    def parse_contents(self, response):
        urlList = response.css('div#contents > div#bo_v > div.bo_v_file > a::attr("href")').re("magnet:.*")
        for url in urlList:
            print url
        #f = open(url,'wb')
        #urlResponse = urllib2.urlopen(url)
        #f.write(urlResponse.read())
        #f.close()
        command = "transmission-remote 9091 -a " + url
        os.system(command.encode('utf-8'))

        yield {'url' : url}

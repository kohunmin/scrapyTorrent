import scrapy

from datetime import datetime

from tutorial.items import TobestItem


class TobestSpider(scrapy.Spider):
    name = "tobogo"
    allowed_domains = ["zipbogo.net"]
    start_urls = [
#        "http://www.zipbogo.net/cdsb/board.php?category=&board=kentertain&search=subject&keyword=1%EB%B0%95"
        "https://zipbogo.net/cdsb/board.php?board=kentertain"
    ]


    def parse(self, response):
        # print response.body
        # Urllist = response.css('div#bo_l_list > table > tbody > tr > td.td_subject > a::attr("href")')
        Urllist = response.css('table.board01 > tbody > tr > td > a::attr("href")').re('board.php.*')
        # print Urllist
        # for url in Urllist.re("/bbs/board.php.*"):
        for url in Urllist:
            yield scrapy.Request(response.urljoin(url), self.parse_contents)


    def parse_contents(self, response):
        # print response.body

        title = response.css('table.board01 > thead > tr > th.end::text').extract()
        downUrl = response.css('table.board01 > tbody.num > tr > td.end > a::attr("href")').re('.*torrent')
        filePaths = response.css('table.board01 > tbody.num > tr > td.end > a > span::text').extract()
        # print filePaths
        # print downUrl

        # urlList = response.css('div#contents > div#bo_v > div.bo_v_file > a::attr("href")').re("magnet:.*&")
        # filePaths = response.css('div#contents > div#bo_v > div.bo_v_file > a::text').re(".*torrent")
        # hit = response.css('div#contents > div#bo_v > div.bo_v_info > td.td_info_right::text').re("[")
        # print hit
        # createTime = response.css('div#contents > div#bo_v > div.bo_v_torrent > table > tr > td.value::text').re("[0-9]{4}-[0-9]{2}-[0-9]{2}.*")
        # command = "transmission-remote 9091 -w " + self.path + " -a " + urlList[0]
        # nowDateTime = datetime.now()
        # createDateTime = datetime.strptime(createTime[0],'%Y-%m-%d %H:%M:%S')
        # diffSeconds = ( nowDateTime - createDateTime ).total_seconds()
        item = TobestItem()
        item['title'] = title
        item['url'] = response.request.url.encode("utf-8")
        if len(downUrl) != 0:
            item['downUrlFile'] = response.urljoin(downUrl[0])
        item['file_paths'] = filePaths[0] + ".torrent"
        # item['hit'] = hit
        # item['createTime'] = createTime
        # item['diffSeconds'] = diffSeconds
        #
        yield item
        # if diffSeconds < self.seconds :
        #     print "INFOTORRENT [torrent]torrent download start"
        #     print "INFOTORRENT title : " + title[0].encode("utf-8").strip()
        #     print "\nINFOTORRENT url : " + response.request.url.encode("utf-8")
        #     print "\nINFOTORRENT command : " + command.encode("utf-8")
        #     print "\nINFOTORRENT creatTime : " + createTime[0]
        #     print "\nINFOTORRENT diff seconds : " + str(diffSeconds)
        #     os.system(command.encode('utf-8'))
        #
        # yield {"title" : title[0].encode("utf-8").strip(), "url" : response.request.url.encode("utf-8") , "command" : command.encode("utf-8"), "createTime" : createTime[0] , "seconds" : diffSeconds }

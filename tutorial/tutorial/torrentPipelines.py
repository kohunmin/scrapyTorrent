import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

class TorrentPipelines(FilesPipeline):
    def get_media_requests(self, item, info):
        file_url = item['downUrlFile']
        yield scrapy.Request(file_url, meta={
            'referer':item['url']
        })

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no images")
        item['file_paths'] = file_paths
        return item
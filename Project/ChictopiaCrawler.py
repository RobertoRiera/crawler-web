import FileManager
import requests
from LinkManager import LinkManager
from time import sleep


class ChictopiaCrawler:
    def __init__(self, init, end):
        self.base_url = 'http://www.chictopia.com/browse/people'
        FileManager.FileManager().create_tag_directory()
        self.tags = FileManager.get_tags_from_file()
        self.parser = LinkManager()
        self.download_page_range(init, end)
        self.parser.download_images_with_tag(self.tags)

    def download_page_range(self, init, end):
        for i in range(init, end):
            actual_url = self.base_url + '/' + str(i)
            html = requests.get(actual_url).text
            sleep(0.1)
            self.parser.feed(html)

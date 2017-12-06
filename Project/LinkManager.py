from html.parser import HTMLParser
from urllib.parse import urljoin
import ImageDownloader


class LinkManager(HTMLParser):
    all_image_links = set()
    special_links = set()

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if '/photo/show/' in str(attr[1]):
                    attri = urljoin('http://www.chictopia.com/', attr[1])
                    self.all_image_links.add(attri)

    def get_links(self):
        return self.all_image_links

    def download_images_with_tag(self, tags):
        for tag in tags:
            for link in self.all_image_links:
                if tag[:-1] in link[35:]:
                    print(link, tag[:-1], link[36:43])
                    ImageDownloader.ImageDownloader(link, tag[:-1], link[36:43])

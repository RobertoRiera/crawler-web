from html.parser import HTMLParser
import requests


class ImageDownloader(HTMLParser):
    def __init__(self, url, tag, name):
        HTMLParser.__init__(self)
        html = requests.get(url).text
        self.name = name
        self.tag = tag
        self.feed(html)

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src' and '400.jpg' in attr[1]:
                    path = 'Photos/' + self.tag + '/undefined/' + self.name + '.jpg'
                    page = requests.get(attr[1])
                    with open(path, 'wb') as image:
                        image.write(page.content)

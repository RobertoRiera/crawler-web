import os


class FileManager:
    def __init__(self):
        self.tags = get_tags_from_file()

    def create_tag_directory(self):
        project_path = os.path.realpath(".")
        tag_path = os.path.join(project_path, 'Photos')
        if not os.path.exists(tag_path):
            os.mkdir('Photos')
            for tag in self.tags:
                last_path = os.path.join(tag_path, tag[:-1])
                os.mkdir(last_path)
                os.mkdir(os.path.join(last_path, "man"))
                os.mkdir(os.path.join(last_path, "woman"))
                os.mkdir(os.path.join(last_path, "undefined"))
        else:
            for tag in self.tags:
                last_path = os.path.join(tag_path, tag[:-1])
                if not os.path.exists(last_path):
                    os.mkdir(last_path)
                if not os.path.exists(os.path.join(last_path, "man")):
                    os.mkdir(os.path.join(last_path, "man"))
                if not os.path.exists(os.path.join(last_path, "woman")):
                    os.mkdir(os.path.join(last_path, "woman"))
                if not os.path.exists(os.path.join(last_path, "undefined")):
                    os.mkdir(os.path.join(last_path, "undefined"))


def get_tags_from_file():
    return open('tags.txt', 'r')

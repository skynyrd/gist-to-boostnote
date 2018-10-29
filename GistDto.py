class GistDto(object):
    def __init__(self, id, files, description):
        self.description = description
        self.id = id
        self.files = files


class GistFileDto(object):
    def __init__(self, file_name, url):
        self.url = url
        self.file_name = file_name
        self.content: str = None

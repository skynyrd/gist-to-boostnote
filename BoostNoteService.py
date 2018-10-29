import ujson
import uuid
from datetime import datetime

from Exceptions import CannotFindFolderKeyError


class BoostNoteService(object):
    def __init__(self, boost_note_path, virtual_folder_name):
        self.virtual_folder_name = virtual_folder_name
        self.folder_path = boost_note_path

    def get_folder_key(self, folder_name):
        config_path = f'{self.folder_path}/boostnote.json'
        with open(config_path) as fd:
            for folder in ujson.load(fd)['folders']:
                if folder["name"] == folder_name:
                    return folder["key"]
        raise CannotFindFolderKeyError(config_path, folder_name)

    def create_files(self, gists):
        folder_key = self.get_folder_key(self.virtual_folder_name)

        for gist in gists:
            for i in range(0, len(gist.files)):
                tag = "[]"
                if len(gist.files) > 1:
                    tag = f'["Gist {gist.id}"]'
                with open(f'{self.folder_path}/{uuid.uuid4()}.cson', 'w') as file:
                    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                    file.write(f"createdAt: \"{current_time}\"\n")
                    file.write(f"updatedAt: \"{current_time}\"\n")
                    file.write(f"type: \"MARKDOWN_NOTE\"\n")
                    file.write(f"folder: \"{folder_key}\"\n")
                    file.write(f"title: \"{gist.files[i].file_name}\"\n")
                    file.write(f"content: '''\n")
                    file.write(gist.files[i].content)
                    file.write("\n")
                    file.write("'''\n")
                    file.write(f'tags: {tag}\n')
                    file.write("isStarred: false\n")
                    file.write("isTrashed: false")

import ujson
import uuid
from datetime import datetime
from pathlib import Path


from Exceptions import CannotFindFolderKeyError
from language_ext_map import language_ext_map


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
            with open(f'{self.folder_path}/gist-{uuid.uuid4()}.cson', 'w') as file:
                current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                file.write(f"createdAt: \"{current_time}\"\n")
                file.write(f"updatedAt: \"{current_time}\"\n")
                file.write(f"type: \"SNIPPET_NOTE\"\n")
                file.write(f"folder: \"{folder_key}\"\n")
                file.write(f"title: \"{gist.description}\"\n")
                file.write(f"description: \"{gist.description}\"\n")
                file.write("snippets: [\n")
                for gist_file in gist.files:
                    not_supported = False
                    extension = Path(gist_file.file_name).suffix[1:]
                    if extension not in language_ext_map:
                        not_supported = True
                    language = "text" if not_supported else language_ext_map[extension]
                    file.write("  {\n")
                    file.write(f'    name: "{gist_file.file_name}"\n')
                    file.write(f'    mode: "{language}"\n')
                    file.write(f"    content: '''\n")
                    file.write(gist_file.content)
                    file.write("\n")
                    file.write("'''\n")
                    file.write("  }\n")
                file.write("]\n")
                file.write(f'tags: []\n')
                file.write("isStarred: false\n")
                file.write("isTrashed: false")

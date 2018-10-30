import asyncio
import sys

from src.BoostNoteService import BoostNoteService
from src.GistApiClient import GistApiClient

if len(sys.argv) != 4:
    print("Usage: gist-to-boostnote.py /path/to/your/boostnote/folder GITHUB_USER_NAME BoostNoteVirtualFolderName")
    exit(True)

retry_count = 3
user_name = sys.argv[2]
boost_note_path = sys.argv[1]
virtual_folder_name = sys.argv[3]

client = GistApiClient(user_name, retry_count)
note_service = BoostNoteService(boost_note_path, virtual_folder_name)

if not note_service.get_folder_key():
    print(f"Cannot find folder <{virtual_folder_name}> in your boostnote.json, "
          f"are you sure that you created it?")
    exit(True)


loop = asyncio.get_event_loop()
future = asyncio.ensure_future(client.get_user_gists())
gists = loop.run_until_complete(future)

note_service.create_files(gists)
print("That's all, restart Boostnote :)")


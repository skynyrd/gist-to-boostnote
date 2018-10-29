import asyncio
from datetime import datetime

from BoostNoteService import BoostNoteService
from GistApiClient import GistApiClient

retry_count = 3
user_name = "skynyrd"
boost_note_path = "/Users/skynyrd/Boostnote"

client = GistApiClient(user_name, retry_count)
note_service = BoostNoteService(boost_note_path, "DenemeBoostNote")

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(client.get_user_gists())
gists = loop.run_until_complete(future)

note_service.create_files(gists)



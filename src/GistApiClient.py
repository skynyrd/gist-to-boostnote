import asyncio

import aiohttp
from typing import List

from src.GistDto import GistDto, GistFileDto


class GistApiClient(object):
    def __init__(self, user_name, retry_count):
        self.retry_count = retry_count
        self.user_name = user_name

    async def fetch_with_retry(self, url, session, rc, json_result):
        if rc > 0:
            try:
                async with session.get(url, ssl=False) as resp:
                    if resp.status != 200:
                        rc -= 1
                        print(f"Can't get result from {url}. {rc} attempt left")
                        await asyncio.sleep(1)
                        return await self.fetch_with_retry(url, session, rc, json_result)
                    else:
                        return await resp.json() if json_result else await resp.text()
            except Exception as e:
                print(e)
        else:
            return None

    async def assign_content(self, gist_file, session, retry_cnt):
        gist_file.content = await self.fetch_with_retry(gist_file.url, session, retry_cnt, False)

    async def get_user_gists(self) -> (List[GistFileDto]):
        async with aiohttp.ClientSession() as session:
            user_gists_resp = await self.fetch_with_retry(f"https://api.github.com/users/{self.user_name}/gists",
                                                          session,
                                                          self.retry_count, True)

            tasks = []
            gists = []

            for gist in user_gists_resp:
                files = []
                for key in gist["files"]:
                    gist_file_dto = GistFileDto(key, gist["files"][key]["raw_url"])
                    tasks.append(asyncio.ensure_future(self.assign_content(gist_file_dto, session, self.retry_count)))
                    files.append(gist_file_dto)
                gists.append(GistDto(gist["id"], files, gist["description"]))

            await asyncio.gather(*tasks)
            return gists

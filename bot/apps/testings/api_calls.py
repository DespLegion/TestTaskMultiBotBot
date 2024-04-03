import aiohttp
import json
from bot.utils import BaseBackendAPI


class TestingsAPI(BaseBackendAPI):
    def __init__(self):
        super().__init__()

    async def get_new_testing(self):
        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.get(f"{self.base_url}/testing") as r:
                res = await r.content.read()
                json_res = json.loads(res)
                return json_res['testing']

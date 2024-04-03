import aiohttp
import json
from bot.utils import BaseBackendAPI


class ServiceAPI(BaseBackendAPI):
    def __init__(self):
        super().__init__()

    async def ping_backend(self):
        try:
            async with aiohttp.ClientSession(headers=self.headers) as s:
                async with s.get(f"{self.base_url}/status") as r:
                    if r.status == 200:
                        res = await r.content.read()
                        json_res = json.loads(res)
                        return json_res["message"]
                    else:
                        return False
        except Exception as err:
            return False

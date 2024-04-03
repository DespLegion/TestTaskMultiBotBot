import aiohttp
import json
from bot.utils import BaseBackendAPI


class PhotoEAPI(BaseBackendAPI):
    def __init__(self):
        super().__init__()

    async def get_watermark(self, user_id):
        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.get(f"{self.base_url}/watermark/{user_id}") as r:
                if r.status == 200:
                    res = await r.read()
                    return res
                else:
                    return f"Some error. Status code: {r.status}"

    async def update_watermark(self, user_id, watermark_img):

        mod_headers = self.headers.copy()
        del mod_headers["Content-Type"]

        watermark_payload = {
            "watermark_img": watermark_img
        }

        async with aiohttp.ClientSession(headers=mod_headers) as s:
            async with s.patch(f"{self.base_url}/watermark/{user_id}", data=watermark_payload) as r:
                if r.status == 200:
                    res = await r.content.read()
                    json_res = json.loads(res)
                    return json_res
                else:
                    return f"Some error. Status code: {r.status}"

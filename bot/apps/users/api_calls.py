import aiohttp
import json
from bot.utils import BaseBackendAPI


class UserAPI(BaseBackendAPI):
    def __init__(self):
        super().__init__()

    async def user_exists(self, user_id):
        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.get(f"{self.base_url}/user/e/{user_id}") as r:
                res = await r.content.read()
                json_res = json.loads(res)
                return json_res['user_exists']

    async def get_user(self, user_id):
        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.get(f"{self.base_url}/user/{user_id}") as r:
                res = await r.content.read()
                json_res = json.loads(res)
                return json_res

    async def create_user(self, user_id: int, user_firstname: str, user_username: str = None, user_lastname: str = None):
        user_payload = {
            "user_id": user_id,
            "user_username": user_username,
            "user_firstname": user_firstname,
            "user_lastname": user_lastname,
        }

        user_json_data = json.dumps(user_payload)

        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.post(f"{self.base_url}/user/", data=user_json_data) as resp:
                return resp.status

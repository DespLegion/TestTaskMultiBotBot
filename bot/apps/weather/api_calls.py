import aiohttp
import json
from bot.utils import BaseBackendAPI


class WeatherAPI(BaseBackendAPI):
    def __init__(self):
        super().__init__()

    async def get_user_last_loc_name(self, user_id):
        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.get(f"{self.base_url}/user/loc/{user_id}") as r:
                res = await r.content.read()
                json_res = json.loads(res)
                return json_res["last_location"]["city"]

    async def update_user_last_loc(self, user_id, city_name: str = None, latitude: float = None, longitude: float = None):
        location_payload = {
            "city": city_name,
            "latitude": latitude,
            "longitude": longitude,
        }

        location_json_data = json.dumps(location_payload)

        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.post(f"{self.base_url}/user/loc/{user_id}", data=location_json_data) as r:
                res = await r.content.read()
                json_res = json.loads(res)
                return json_res["new_loc"]

    async def get_weather(self, user_id):
        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.get(f"{self.base_url}/weather/{user_id}") as r:
                res = await r.content.read()
                comp_res = json.loads(res)["weather"]
                if not comp_res == "Some error":
                    comp_res["city"] = json.loads(res)["city"]
                    return comp_res
                else:
                    return "Unknown place"

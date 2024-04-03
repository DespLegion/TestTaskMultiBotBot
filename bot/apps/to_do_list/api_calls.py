import aiohttp
import json
from bot.utils import BaseBackendAPI


class ToDoAPI(BaseBackendAPI):
    def __init__(self):
        super().__init__()

    async def get_all_user_tasks(self, user_id: int):
        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.get(f"{self.base_url}/to_do/{user_id}") as r:
                res = await r.content.read()
                json_res = json.loads(res)
                return json_res

    async def create_user_task(self, user_id: int, task_title: str, task_text: str):
        task_payload = {
            "task_title": task_title,
            "task_text": task_text
        }
        task_json = json.dumps(task_payload)
        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.post(f"{self.base_url}/to_do/{user_id}", data=task_json) as r:
                res = await r.content.read()
                json_res = json.loads(res)
                return json_res

    async def get_user_task(self, user_id: int, task_id: int):
        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.get(f"{self.base_url}/to_do/{user_id}/{task_id}") as r:
                res = await r.content.read()
                json_res = json.loads(res)
                return json_res

    async def update_user_task(self, user_id: int, task_id: int, task_title: str = None, task_text: str = None):
        if task_title is None:
            task_title = ""
        if task_text is None:
            task_text = ""
        task_payload = {
            "task_title": task_title,
            "task_text": task_text
        }
        task_json = json.dumps(task_payload)
        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.patch(f"{self.base_url}/to_do/{user_id}/{task_id}", data=task_json) as r:
                res = await r.content.read()
                json_res = json.loads(res)
                return json_res

    async def delete_user_task(self, user_id: int, task_id: int):
        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.delete(f"{self.base_url}/to_do/{user_id}/{task_id}") as r:
                res = await r.content.read()
                json_res = json.loads(res)
                return json_res

import config


class BaseBackendAPI:
    def __init__(self):
        self.base_url = f"{config.BACKEND_BASE_URL}/api"
        self.headers = {
            'Authorization': config.BACKEND_TOKEN,
            'User-Agent': config.BOT_AGENT,
            'Content-Type': 'application/json'
        }

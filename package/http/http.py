import requests
import json
from typing import Optional, Dict
from config.config import Config

class HttpClient:
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}

    def get(self, path: str, params: Optional[Dict[str, str]] = None) -> requests.Response:
        url = self._build_url(path, params)
        return requests.get(url, headers=self.headers)

    def post(self, path: str, data: Optional[Dict[str, str]] = None, json_data: Optional[Dict[str, str]] = None) -> requests.Response:
        url = self._build_url(path)
        return requests.post(url, data=data, json=json_data, headers=self.headers)

    def put(self, path: str, data: Optional[Dict[str, str]] = None, json_data: Optional[Dict[str, str]] = None) -> requests.Response:
        url = self._build_url(path)
        return requests.put(url, data=data, json=json_data, headers=self.headers)

    def delete(self, path: str) -> requests.Response:
        url = self._build_url(path)
        return requests.delete(url, headers=self.headers)

    def _build_url(self, path: str, params: Optional[Dict[str, str]] = None) -> str:
        url = f"{self.base_url}/{path.lstrip('/')}"
        if params:
            query_params = '&'.join(f"{key}={value}" for key, value in params.items())
            url += f"?{query_params}"
        return url
    def post_to_azure_open_ai(message: str):
        endpoint = Config.AZURE_OPENAI_ENDPOINT
        api_key = Config.AZURE_OPENAI_KEY
        deployment = Config.AZURE_OPENAI_CHATGPT_DEPLOYMENT
        api_version = Config.AZURE_OPENAI_API_VERSION
        api_url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        headers = {
            'Content-Type': 'application/json',
            'api-key': api_key
        }
        
        return api_url, payload, headers

def decode(response: requests.Response) -> Optional[Dict]:
    try:
        return response.json()
    except json.JSONDecodeError:
        return None

def encode(data: Dict) -> Optional[bytes]:
    try:
        return json.dumps(data).encode('utf-8')
    except TypeError:
        return None

import logging
from typing import Optional, Dict, Any
import requests
from .config import API_BASE_URL

log = logging.getLogger("jobbot")

def api_get(path: str, params: Optional[Dict[str, Any]] = None) -> Optional[dict]:
    try:
        url = f"{API_BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        log.error("API error: %s", e)
        return None

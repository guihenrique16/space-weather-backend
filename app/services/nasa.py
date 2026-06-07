import requests
from app.core.config import NASA_API_KEY

BASE_URL = "https://api.nasa.gov/DONKI"

def get_solar_flares(start_date: str = None, end_date: str = None) -> list:
    """Busca Solar Flares (FLR) dos últimos 30 dias por padrão."""
    params = {"api_key": NASA_API_KEY}
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date

    response = requests.get(f"{BASE_URL}/FLR", params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def get_geomagnetic_storms(start_date: str = None, end_date: str = None) -> list:
    """Busca Geomagnetic Storms (GST)."""
    params = {"api_key": NASA_API_KEY}
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date

    response = requests.get(f"{BASE_URL}/GST", params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def get_cme(start_date: str = None, end_date: str = None) -> list:
    """Busca Coronal Mass Ejections (CME)."""
    params = {"api_key": NASA_API_KEY}
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date

    response = requests.get(f"{BASE_URL}/CME", params=params, timeout=10)
    response.raise_for_status()
    return response.json()

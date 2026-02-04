from fastapi import FastAPI, HTTPException
import requests
from settings import get_settings

app = FastAPI()


@app.get("/")
async def read_root():
    settings = get_settings()
    return {"Hello": "World"}


@app.get("/ip/{ip}")
async def geolookup(ip: str):
    print(f"DEBUG: Processing IP {ip}")
    try:
        settings = get_settings()
        base = settings.circl_api_url.rstrip("/")
        url = f"{base}/geolookup/{ip}"
        print(f"DEBUG: Requesting {url}")

        r = requests.get(url, timeout=5)
        print(f"DEBUG: Response status: {r.status_code}")
        r.raise_for_status()

        raw_data = r.json()
        print(f"DEBUG: Data type: {type(raw_data)}")

        # Validation strict structure CIRCL : List[Dict]
        if not isinstance(raw_data, list) or len(raw_data) == 0:
            raise ValueError("CIRCL response is not a valid list or is empty")

        first_entry = raw_data[0]
        country_info = first_entry.get("country_info")

        if not isinstance(country_info, dict):
            raise ValueError("'country_info' missing or not a dict")

        country = country_info.get("Country", "Unknown")

        # Conversion et validation des types
        try:
            lat = float(country_info.get("Latitude (average)"))
            lon = float(country_info.get("Longitude (average)"))
        except (TypeError, ValueError):
            raise ValueError("Latitude/Longitude invalid or missing")

    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"DEBUG: Exception: {e}")
        raise HTTPException(
            status_code=502, detail=f"CIRCL error or parsing failed: {e}"
        )

    return {
        "ip": ip,
        "country": country,
        "latitude": lat,
        "longitude": lon,
    }

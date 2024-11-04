"""Module for time generating"""
from datetime import datetime, timedelta
from fastapi import FastAPI
import requests

VERSION = "v0.0.2"
time_now = datetime.utcnow()
hour_earlier = time_now - timedelta(hours=1)
F_hour_earlier = hour_earlier.isoformat(timespec='seconds') + 'Z'
BOXID="5eba5fbad46fb8001b799786"
SENSORID="5eba5fbad46fb8001b799789"

print (F_hour_earlier)

app = FastAPI()

@app.get("/version")
async def version():
    """returns app version"""
    return VERSION

@app.get("/temperature")
async def temp():
    """returns temperature from specific box for the last hour"""
    url = f"https://api.opensensemap.org/boxes/{BOXID}/data/{SENSORID}?from-date={F_hour_earlier}"
    test=requests.get(url,timeout=30)
    return test.json()

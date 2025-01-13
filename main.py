"""Module for time generating"""
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests


APP_VERSION="v0.0.5"
time_now = datetime.utcnow()
hour_earlier = time_now - timedelta(hours=1)
F_hour_earlier = hour_earlier.isoformat(timespec='milliseconds') + 'Z'
BOXID = "579e683668b4a21200661a6d"
SENSORID ="579e683668b4a21200661a73"
values = []

app = FastAPI()

@app.get("/",response_class=HTMLResponse)
async def main():
    """returns main page"""
    return """
    <html>
        <body>
            <h1>Welcome to our App</h1>
        </body> 
    </html>
    """

@app.get("/version")
async def version():
    """returns app version"""
    return APP_VERSION

@app.get("/temperature")
async def temp():
    """returns temperature from specific box for the last hour"""
    url = f"https://api.opensensemap.org/boxes/{BOXID}/data/{SENSORID}?from-date={F_hour_earlier}"
    request=requests.get(url,timeout=30)
    temp_values = request.json()
    for item in temp_values:
        values.append(item['value'])
    values_float=list(map(float, values))
    avg_temp = sum(values_float) / len (values_float)
    rounded_avg_temp=round(avg_temp,0)
    if rounded_avg_temp < 10:
        status = "Too Cold"
    elif 10 <= rounded_avg_temp < 36:
        status = "Good"
    else:
        status = "Too Hot"
    return "average Temperature: " + str(rounded_avg_temp) + " & the status is: " + status




@app.get("/metrics")
async def metrics():
    """returns metrics"""
    return "This part is still under construction"

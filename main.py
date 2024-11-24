"""Module for time generating"""
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from kubernetes import client, config
import requests


config.load_kube_config()
v1 = client.CoreV1Api()
ret = v1.list_pod_for_all_namespaces(watch=False)
APP_VERSION="v0.0.4"
time_now = datetime.utcnow()
hour_earlier = time_now - timedelta(hours=1)
F_hour_earlier = hour_earlier.isoformat(timespec='seconds') + 'Z'
BOXID = "eba5fbad46fb8001b799786"
SENSORID ="5eba5fbad46fb8001b799789"
values = []
X = []
app = FastAPI()

@app.get("/",response_class=HTMLResponse)
async def main():
    """returns main page"""
    return """
    <html>
        <body>
            <h1> Welcome to our app </h1>
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
    elif rounded_avg_temp >= 10 & rounded_avg_temp < 36:
        status = "Good"
    else:
        status = "Too Hot"
    return "average Temperature: " + str(rounded_avg_temp) + " & the status is: " + status




@app.get("/metrics")
async def metrics():
    """returns metrics"""
    # http://127.0.0.1:8001/apis/metrics.k8s.io/v1beta1/pods?labelSelector=k8s-app%3Dkube-dns
    for i in ret.items:
        X.append([i.status.pod_ip, i.metadata.namespace, i.metadata.name])
    return X

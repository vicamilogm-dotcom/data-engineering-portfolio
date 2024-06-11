import asyncio
import time
from datetime import datetime

from fastapi import FastAPI


app = FastAPI()

# Add a unique app_instance_id, which changes every time the app is started
app_instance_id = str(datetime.utcnow())


@app.get("/say-hi")
async def root():
    await asyncio.sleep(0.2)
    return {"message": "Hello World", "time": time.time()}


@app.get("/fast-run")
async def fast_run():
    payload = {"app_instance_id": app_instance_id}
    await asyncio.sleep(2)
    return payload


@app.get("/slow-run")
async def slow_run():
    payload = {"app_instance_id": app_instance_id}
    time.sleep(2)
    return payload


@app.get("/standard-run")
def standard_run():
    payload = {"app_instance_id": app_instance_id}
    time.sleep(2)
    return payload

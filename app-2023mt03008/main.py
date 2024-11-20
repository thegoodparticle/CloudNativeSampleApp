import time
from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
from prometheus_client import Counter, Gauge, Histogram, generate_latest
import os

import psutil

# initialize the application
app = FastAPI()

# Traffic (request count)
REQUEST_COUNT = Counter("getinfo_request_count", "Total number of requests")

# Latency (request latency)
REQUEST_LATENCY = Histogram("getinfo_request_latency_seconds", "Request latency")

# CPU utilization as a Gauge
CPU_UTILIZATION = Gauge("getinfo_cpu_utilization", "CPU utilization in percentage")

# Memory utilization as a Gauge
MEMORY_UTILIZATION = Gauge("getinfo_mem_utilization", "Memory utilization in percentage")

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    if request.url.path == "/get_info":
        # Start timer  
        start_time = time.time()
        # Process the request
        response = await call_next(request)
        # Update metrics
        REQUEST_COUNT.inc() # Increment request count

        latency = time.time() - start_time
        REQUEST_LATENCY.observe(latency) # Record latency

        CPU_UTILIZATION.set(psutil.cpu_percent(interval=None)) # Update CPU utilization

        MEMORY_UTILIZATION.set(psutil.virtual_memory().percent) # Update Memory utilization
    else:
        # Process the request
        response = await call_next(request)
    
    return response

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")

# endpoint '/get_info' definition
@app.get("/get_info")
def get_info():
    # load the values in configs/.env file into env variables
    load_dotenv()
    
    # get the indended app version and title from env vars
    app_version = os.getenv("APP_VERSION")
    app_title = os.getenv("APP_TITLE")
    
    return {
        "version": app_version, 
        "title": app_title
    }

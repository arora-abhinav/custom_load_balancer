from fastapi import FastAPI, HTTPException
import requests
import httpx
import asyncio

url_8001 = "http://0.0.0.0:8001/"
url_8002 = "http://0.0.0.0:8002/"
url_8000 = "http://0.0.0.0:8000/"

urls = [url_8002, url_8001, url_8000]

async def health_request(url):
    #This is wrapped in a try except block to prevent the error from bubbling up and stopping 
    #all other tasks in the main function
    try:
        #This specific context manager is used to dish out requests asynchronously. 
        async with httpx.AsyncClient() as client:
            #await is required here because client.get is running as an async def under the hood. Calling it without await 
            #simply means the response is actually couroutine object that is simply being waited to be run
            response = await client.get(url)
    except httpx.ConnectError as e:
        response = {"Health": False}
    return response
        
async def health_endpoint_scheduler():
    tasks = []
    #Task Group merges tasks together to run asynchronously. Exits when all tasks are done
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            task = tg.create_task(health_request(url))
            tasks.append(task)

    print("Hit all endpoints")

async def main(sleep_time):
    while True:
        await asyncio.sleep(sleep_time)
        await health_endpoint_scheduler()

#Bridges the gap between asynchronous running and synchronous execution
#Concurrently hitting the endpoints
asyncio.run(main(3))

#This function is for simply forwarding a request to a specific worker
async def forward_request(url):
    try:
        async with httpx.AsyncClient() as client:
            respose = client.get(url)
    except httpx.RequestError as e:
        print("Oops:", e)
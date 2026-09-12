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
        
async def main():
    tasks = []
    #Task Group merges tasks together to run asynchronously. Exits when all tasks are done
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            task = tg.create_task(health_request(url))
            tasks.append(task)

    print("Hit all endpoints")

#Bridges the gap between asynchronous running and synchronous execution
asyncio.run(main())

"""try:
    for url in urls:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Incorrect URL or Username not found")
        else:
            print(response.json())
except Exception:
    print("Failed")
"""
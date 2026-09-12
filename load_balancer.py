from fastapi import FastAPI, HTTPException
import requests

url_8001 = "http://0.0.0.0:8001/get_user_tier/u_1010"
url_8002 = "http://0.0.0.0:8002/get_user_tier/u_1010"
url_8000 = "http://0.0.0.0:8000/get_user_tier/u_1010"

urls = [url_8002, url_8001, url_8000]

try:
    for url in urls:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Incorrect URL or Username not found")
        else:
            print(response.json())
except Exception:
    print("Failed")



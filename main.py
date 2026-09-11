from fastapi import FastAPI, Request, Response, Body, Query, Path
from pydantic import BaseModel

app = FastAPI()

#See if servers are up and running
@app.get("/health")
async def health():
    return {"Health": True}



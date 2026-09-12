from fastapi import FastAPI, Request, Response, Body, Query, Path, HTTPException
from pydantic import BaseModel

app = FastAPI()

#User accounts and their tiers
ACCOUNT_TIERS = {
    "u_1001": "free",
    "u_1002": "pro",
    "u_1003": "enterprise",
    "u_1004": "free",
    "u_1005": "pro",
    "u_1006": "free",
    "u_1007": "enterprise",
    "u_1008": "pro",
    "u_1009": "free",
    "u_1010": "enterprise",
}

#See if servers are up and running
@app.get("/health")
async def health():
    return {"Health": True}

@app.get("/get_user_tier/{user_id}")
async def get_user_tier(request: Request, user_id: str = Path(description="User ID to indicate their tier")):
    if user_id not in ACCOUNT_TIERS:
        return HTTPException(status_code=404, detail="Invalid User")
    #Port returns which port the current FastAPI instance is running on
    return {"User Tier": ACCOUNT_TIERS[user_id], "Port": request.url.port}


#Running Test instances on ports 8000, 8001, 8002

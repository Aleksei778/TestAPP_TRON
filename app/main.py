from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import TronAddressQueryRead, TronAddressQueryCreate
from .tron_service import TronService
from .database import get_db_conn
from .db_manager import DBManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_router = APIRouter(prefix="/api/v1")
app = FastAPI()
tron_service = TronService()

origins = [
    "http://127.0.0.1:8000"
]
methods = [
    "GET", 
    "POST"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Authorization", "Access-Control-Allow-Origins", "accept"]
)

app.include_router(api_router)

@app.post("/tron-info", response_model=TronAddressQueryCreate)
async def get_tron_address_info_and_save_to_db(address: str, db: AsyncSession = Depends(get_db_conn)):
    db_manager = DBManager(session=db)
    
    wallet_info = tron_service.get_wallet_info(address=address)
    
    if not wallet_info:
        raise HTTPException(status_code=404, detail="Such address was not found")

    balance = wallet_info['balance']
    energy = wallet_info['energy']
    bandwidth = wallet_info['bandwidth']
    
    tron_query = await db_manager.add_tron_info_to_db(address=address, balance=balance, bandwidth=bandwidth, energy=energy)

    return tron_query

@app.get("/tron-info", response_model=List[TronAddressQueryRead])
async def get_recent_tron_queries_from_db(offset: int, limit: int, db: AsyncSession = Depends(get_db_conn)):
    db_manager = DBManager(session=db)

    result = await db_manager.get_tron_info_from_db(offset=offset, limit=limit)

    return result

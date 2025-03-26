import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import TronAddressQuery
from app.database import SessionLocal

@pytest.fixture
def test_tron_data():
    test_tron_data = {
        "address": "TNaRAoLUyYEV2uFZdZULU5H8KZ1sZo76fy",
        "balance_trx": 100.5,
        "bandwidth": 1500.0,
        "energy": 2000.0
    }

    return test_tron_data
    

@pytest.mark.asyncio
async def test_db_write(test_tron_data: dict):
    async with SessionLocal() as db:
        wallet_info = TronAddressQuery(
            address=test_tron_data['address'],
            balance_trx=test_tron_data['balance_trx'],
            bandwidth=test_tron_data['bandwidth'],
            energy=test_tron_data['energy']
        )

        db.add(wallet_info)
        await db.commit()
        await db.refresh(wallet_info)
            
        result = await db.execute(
            select(TronAddressQuery)
            .where(TronAddressQuery.address == test_tron_data['address'])
        )

        saved_wallet_info = result.scalar_one()

        assert saved_wallet_info is not None
        assert saved_wallet_info.address == test_tron_data['address']
        assert saved_wallet_info.balance_trx == test_tron_data['balance_trx']
        assert saved_wallet_info.bandwidth == test_tron_data['bandwidth']
        assert saved_wallet_info.energy == test_tron_data['energy']
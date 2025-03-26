from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc

from .models import TronAddressQuery

class DBManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_tron_info_to_db(self, address: str, balance: float, energy: float, bandwidth: float):
        new_tron_query = TronAddressQuery(
            address=address,
            balance_trx=balance,
            bandwidth=bandwidth,
            energy=energy
        )

        self.session.add(new_tron_query)
        await self.session.commit()
        await self.session.refresh(new_tron_query)

        return new_tron_query
    
    async def get_tron_info_from_db(self, offset: int = 0, limit: int = 10):
        result = await self.session.execute(
            select(TronAddressQuery)
            .order_by(desc(TronAddressQuery.created_at))
            .offset(offset)
            .limit(limit)
        )

        return result.scalars.all()
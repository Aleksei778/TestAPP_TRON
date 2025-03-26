from tronpy import Tron
from tronpy.providers import HTTPProvider
from typing import Dict

class TronService:
    def __init__(self):
        self.client = Tron(provider=HTTPProvider("https://api.trongrid.io"))

    async def get_wallet_info(self, address) -> Dict:
        try:
            account = await self.client.get_account(addr=address)
            balance = await self.client.get_account_balance(addr=address)

            bandwidth = account.get('bandwith', {}).get('netRemaining', 0)
            energy = account.get('energy', {}).get('energyRemaining', 0)

            return {
                'balance': balance,
                'energy': energy,
                'bandwidth': bandwidth
            }
        except Exception as e:
            print(f"Error during getting info from tron: {str(e)}")
            return None
from aiocryptopay import AioCryptoPay, Networks
import asyncio

from data.config import token

class CryptoBot:
    def __init__(self):
        self.repo = repo
        self.crypto_bot = AioCryptoPay(token=token, network=Networks.MAIN_NET)
        
    def create_check(self, amount: float, user_id: int):
        res = await self.crypto_bot.create_check(asset='USDT', amount=amount, pin_to_user_id=user_id)
                
        return check

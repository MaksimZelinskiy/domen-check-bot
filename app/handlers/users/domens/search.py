import asyncio
import ssl
import socket
import aiohttp
from urllib.parse import urlparse

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters import IsPrivate, IsAdmin
from loader import bot
from database.repo.requests import RequestsRepo

from utils.states import DomainCheckStates

router = Router()

@router.message(Command("search"))
async def command_check_domains(message: Message, state: FSMContext):
    await message.answer("Введите список доменов для проверки (каждый домен с новой строки):\n\n<b>Пример:</b>\nexample.com\nhttp://example.com\nhttps://example.com")
    await state.set_state(DomainCheckStates.waiting_domains)

async def check_domain(domain: str, proxy: str = None, session: aiohttp.ClientSession = None):
    parsed_url = urlparse(domain)
    domain_name = parsed_url.netloc or domain
    
    proxies = {
        'http': proxy,
        'https': proxy
    } if proxy else None

    result = {
        "domain": domain_name,
        "ssl_status": "-",
        "http_status": "-", 
        "availabl": "недоступен"
    }
    
    # проверка домена через сессию
    try:
        async with session.get(
            domain,
            timeout=aiohttp.ClientTimeout(total=5),
            ssl=True,
            proxy=proxies
        ) as response:
            result.update({
                "ssl_status": "OK",
                "http_status": response.status,
                "availabl": "доступен"
            })
                
    except ssl.SSLError:
        result["ssl_status"] = "Ошибка"
    except (aiohttp.ClientError, asyncio.TimeoutError):
        pass

    return result

async def check_domains_batch(domains: list, proxy: str = None) -> list:
    tasks = []

    # создание сессии для проверки пачки доменов
    async with aiohttp.ClientSession() as session:

        # создание задач в пачке
        for domain in domains:
            domain = domain.strip()
                
            # обработка домена
            if domain.startswith('http://'):
                domain = domain.replace('http://', 'https://')
            elif not domain.startswith('https://'):
                domain = f'https://{domain}'

            # создание задачи для проверки домена
            tasks.append(check_domain(domain, proxy, session))
        
        # запуск задач в пачке
        results = await asyncio.gather(*tasks)
        return results

@router.message(DomainCheckStates.waiting_domains)
async def process_domains(message: Message, state: FSMContext):
    text = message.text.strip()
    domains = text.split('\n')
    
    proxy = None # МОКАП для прокси    
    result = []
    
    batch_size = 10 # количество в одной пачке
    domain_batches = [domains[i:i + batch_size] for i in range(0, len(domains), batch_size)]
    
    # оповещение о прокси
    if proxy:
        await message.answer(f"Используется прокси: {proxy}")
    
    for batch in domain_batches:
        batch_results = await check_domains_batch(batch, proxy) # создание + запуск пачки
        
        for domain_result in batch_results: # вывод результата
            result.append(
                f"<b>Домен:</b> {domain_result['domain']}\n"
                f"<b>SSL:</b> {domain_result['ssl_status']}\n"
                f"<b>Статус:</b> {domain_result['http_status']}\n"
                f"<b>Доступ:</b> {domain_result['availabl']}\n"
            )
        
        # пауза между пачками (чтобы не было спама (422))
        await asyncio.sleep(1)
    
    await message.answer("\n".join(result))
    await state.clear()

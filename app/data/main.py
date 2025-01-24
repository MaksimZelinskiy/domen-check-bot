import asyncio
import json
import os
from typing import Union

from aiogram import Bot
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InputMediaPhoto,
    InputFile
)
from aiogram.utils.deep_linking import create_start_link

from filters import IsPrivate
from loader import bot

from data import config

async def download_avatar(user_id: int, bot: Bot) -> None:
    """Download user avatar and save it to file"""
    user_profile_photos = await bot.get_user_profile_photos(user_id)
    
    if user_profile_photos.total_count > 0:
        # Get largest photo size
        photo = user_profile_photos.photos[0][-1]
        file = await bot.get_file(photo.file_id)
        
        # Download and save file
        file_name = f"{user_id}.jpg"
        await bot.download_file(file.file_path, f"/opt/folder/users/{file_name}")

async def get_keyboard_menu(user_id: int) -> InlineKeyboardMarkup:
    """Generate menu keyboard with referral link"""
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Пригласить друга",
            url=f"https://t.me/share/url?url={await create_start_link(bot, user_id)} 👋 Вот моя реферальная ссылка на DreamCoin.\nЗарабатывай вместе со мной!"
        )]
    ])
    return markup

async def read_json(path: str) -> dict:
    """Read and parse JSON file"""
    async with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

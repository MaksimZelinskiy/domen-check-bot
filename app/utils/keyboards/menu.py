
from aiogram import types


class BuilderKeyboard:
    
    def __init__(self, keyboard_format):
        key_formats = {
            "inline": types.InlineKeyboardMarkup(),
            "reply": types.ReplyKeyboardMarkup()
        }
        
        if keyboard not in key_formats:
            raise 404
        
        self.markup = key_formats[keyboard_format]
    
    
    async def main(user_id, ):
        pass





import os
import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token='8158991088:AAEtFT2L4CjaxXoDXaSF9rROaANMDQxurdA')
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды")

@dp.message_handler()
async def get_weather(message: types.Message):
    city = message.text.strip()
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid=ba11ad96302c9b223efbd105e997cb73"
        )
        data = response.json()
        if response.status_code != 200:
            await message.reply("Не удалось получить погоду. Проверьте название города.")
            return
        # Формируем ответ
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        reply_text = (
            f"Погода в {city}:\n"
            f"{weather_desc.capitalize()}\n"
            f"Температура: {temp}°C\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )
        await message.reply(reply_text)
    except:
        await message.reply("Произошла ошибка при получении данных о погоде.")

if __name__ == "__main__":
    executor.start_polling(dp)

import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши название города!")

@dp.message_handler()
async def get_weather(message: types.Message):
    emoji = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Mist": "Туман \U0001F32B",
        "Snow": "Снег \U0001F328",
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        feels_like = data["main"]["feels_like"]
        wind = data["wind"]["speed"]
        weather_description = data["weather"][0]["main"]

        if weather_description in emoji:
            wd = emoji[weather_description]
        else:
            wd = "Глянь в окно, там не понятно чё"


        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city} {wd}\nТемпература: {cur_weather}°С Ощущается: {feels_like}°С\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм рт.ст.\nСкорость ветра: {wind} м/с\n"
              f"Хорошего дня!")



    except Exception as ex:
        print(ex)
        print("Проверьте название города!")


if __name__ == '__main__':
    executor.start_polling(dp)
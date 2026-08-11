import telebot
import requests
from bs4 import BeautifulSoup
import time


TOKEN = "ТОКЕН"
bot = telebot.TeleBot(TOKEN)

def get_weather_moscow():
    """
    Парсит погоду для бота
    """
    url = "https://yandex.ru/pogoda/moscow"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        temp = soup.find("span", class_="temp__value")
        description = soup.find("div", class_="link__condition")
        
        if temp and description:
            return f"🌡️ {temp.text.strip()}°, {description.text.strip()}"
        else:
            return "Не удалось получить погоду"
    except Exception as e:
        return f"Ошибка: {e}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот-погода. Напиши /weather, чтобы узнать погоду в Москве.")

@bot.message_handler(commands=['weather'])
def send_weather(message):
    bot.send_message(message.chat.id, "Ищу погоду... 🔍")
    weather = get_weather_moscow()
    bot.send_message(message.chat.id, f"Погода в Москве сейчас: {weather}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я понимаю только команды: /start и /weather")

print("Бот запущен...")
bot.polling()

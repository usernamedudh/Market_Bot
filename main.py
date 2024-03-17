import telebot
import requests
from bs4 import BeautifulSoup


TOKEN = '7048254842:AAHHzHhc5ipaQt1Cdm3OLwls_z4IxD0q5OI'


bot = telebot.TeleBot(TOKEN)


def search_category(category_name):
    try:
        category_url = f'https://rozetka.com.ua/ua/{category_name}/'
        response = requests.get(category_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='goods-tile')
        if not items:
            return None
        results = []
        for item in items[:30]:
            title = item.find('span', class_='goods-tile__title').text.strip()
            price = item.find('span', class_='goods-tile__price-value').text.strip()
            link = item.find('a', class_='goods-tile__picture').get('href')
            results.append({'title': title, 'price': price, 'link': link})
        return results
    except Exception as e:
        print("Error:", e)
        return None


@bot.message_handler(func=lambda message: True)
def search_handler(message):
    category_name = message.text
    results = search_category(category_name)
    if not results:
        bot.reply_to(message, "По вашему запросу ничего не найдено.")
    else:
        for result in results:
            response = f"<b>{result['title']}</b>\nЦена: {result['price']} грн\nСсылка: {result['link']}"
            bot.send_message(message.chat.id, response, parse_mode='HTML')

def main():
    bot.polling()

if __name__ == "__main__":
    main()

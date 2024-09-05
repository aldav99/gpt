import telebot
from openai import OpenAI

# Инициализация клиента OpenAI
client = OpenAI(
    api_key="sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I",
    base_url="https://api.proxyapi.ru/openai/v1",
)

# Создаем экземпляр Telegram-бота
bot = telebot.TeleBot("7432911185:AAFQpTAW2LBeclTNCYXc4GCL9fl43YgmAYA")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Отправляем запрос к модели
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "отвечай в стиле веселого клоуна"},
                {"role": "user", "content": message.text}
            ]
        )

        # Получаем ответ от модели
        response = chat_completion.choices[0].message.content

        # Отправляем ответ пользователю
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка: " + str(e))

# Запуск бота
bot.polling()
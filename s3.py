import telebot
from openai import OpenAI
from gtts import gTTS
import os

# Инициализация клиента OpenAI
client = OpenAI(
    api_key="sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I",
    base_url="https://api.proxyapi.ru/openai/v1",
)

# Создаем экземпляр Telegram-бота
bot = telebot.TeleBot("7432911185:AAFQpTAW2LBeclTNCYXc4GCL9fl43YgmAYA")

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
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

        # Преобразуем текст в речь
        tts = gTTS(text=response, lang='ru')
        audio_file = "response.ogg"
        tts.save(audio_file)

        # Отправляем голосовое сообщение пользователю
        with open(audio_file, 'rb') as audio:
            bot.send_voice(message.chat.id, audio)

        # Удаляем временный аудиофайл
        os.remove(audio_file)

    except Exception as e:
        bot.reply_to(message, "Произошла ошибка: " + str(e))

# Обработчик сообщений с документом
@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        # Получаем имя файла
        file_name = message.document.file_name

        # Преобразуем имя файла в речь
        tts = gTTS(text=f"Имя вашего файла: {file_name}", lang='ru')
        audio_file = "filename.ogg"
        tts.save(audio_file)

        # Отправляем голосовое сообщение пользователю
        with open(audio_file, 'rb') as audio:
            bot.send_voice(message.chat.id, audio)

        # Удаляем временный аудиофайл
        os.remove(audio_file)

    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при обработке файла: " + str(e))

# Запуск бота
bot.polling()
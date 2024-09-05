import telebot
from openai import OpenAI
import os
import chardet

API_TOKEN = '7432911185:AAFQpTAW2LBeclTNCYXc4GCL9fl43YgmAYA'
OPENAI_API_KEY = "sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I"

bot = telebot.TeleBot(API_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_text(text):
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{
            "role": "user",
            "content": f"Сделай краткое резюме следующего текста: {text}"
        }]
    )
    response = chat_completion.choices[0].message.content
    return response

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправьте мне текстовый файл, и я сделаю его краткое резюме.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        input_file_path = f"./{message.document.file_name}"

        with open(input_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Автоматическое определение кодировки
        with open(input_file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        # Чтение файла с определенной кодировкой
        with open(input_file_path, 'r', encoding=encoding, errors='replace') as file:
            text = file.read()

        summary = summarize_text(text)
        bot.send_message(message.chat.id, f"Резюме: {summary}")

        os.remove(input_file_path)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

bot.polling()
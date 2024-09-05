import telebot
import os
import subprocess
from openai import OpenAI


API_KEY = '7432911185:AAFQpTAW2LBeclTNCYXc4GCL9fl43YgmAYA'
OPENAI_API_KEY = 'sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I'

bot = telebot.TeleBot(API_KEY)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.proxyapi.ru/openai/v1",
)

def convert_to_mobi(input_file, output_file):
    try:
        subprocess.run(['ebook-convert', input_file, output_file], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Отправьте мне файл в формате PDF, FB2 или EPUB, и я сконвертирую его в MOBI.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        input_file_path = f"./{message.document.file_name}"
        output_file_path = input_file_path.rsplit('.', 1)[0] + '.mobi'

        with open(input_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        if convert_to_mobi(input_file_path, output_file_path):
            with open(output_file_path, 'rb') as mobi_file:
                bot.send_document(message.chat.id, mobi_file)
            os.remove(output_file_path)
        else:
            bot.reply_to(message, "Не удалось конвертировать файл.")

        os.remove(input_file_path)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Отправьте файл для конвертации.")

bot.polling()
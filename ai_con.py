from openai import OpenAI

# Инициализация клиента OpenAI
client = OpenAI(
    api_key="sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I",
    base_url="https://api.proxyapi.ru/openai/v1",
)

def chat_with_ai():
    print("Добро пожаловать в консольный чат с нейросетью!")
    print("Введите 'exit' для завершения.")

    while True:
        # Запрашиваем ввод от пользователя
        user_input = input("Вы: ")

        # Проверяем, не хочет ли пользователь завершить сеанс
        if user_input.lower() == 'exit':
            print("Завершение сеанса.")
            break

        # Отправляем запрос к модели
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "отвечай в стиле веселого клоуна"},
                {"role": "user", "content": user_input}
            ]
        )

        # Получаем ответ от модели
        # response = chat_completion.choices[0].message['content']
        response = chat_completion.choices[0].message.content

        # Выводим ответ
        print(f"AI: {response}")

# Запуск функции для общения
chat_with_ai()
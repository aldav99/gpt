from openai import OpenAI


def main():
    client = OpenAI(
        api_key="sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I",
        base_url="https://api.proxyapi.ru/openai/v1",
    )

    print("Введите 'exit' для завершения программы.")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "exit":
            print("Завершение работы.")
            break

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[{
                "role": "user",
                "content": user_input
            }])

        response = chat_completion.choices[0].message.content
        print(f"Модель: {response}")


if __name__ == "__main__":
    main()

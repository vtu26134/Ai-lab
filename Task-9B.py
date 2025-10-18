import openai

# Set your OpenAI API key
openai.api_key = "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"

messages = []

# Ask user for the type of chatbot to create
system_msg = input("What type of chatbot would you like to create?\n")
messages.append({"role": "system", "content": system_msg})

print("Your new assistant is ready! Type your query (type 'quit()' to exit)")

while True:
    message = input("You: ")
    if message.lower() == "quit()":
        print("Exiting chatbot. Goodbye!")
        break

    messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})

    print("\nAssistant: " + reply + "\n")

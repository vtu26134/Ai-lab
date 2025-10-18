import openai
import gradio as gr

# Set your OpenAI API key
openai.api_key = "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"

# Initialize conversation with system prompt
messages = [
    {"role": "system", "content": "You are a financial expert specializing in real estate investment and negotiation."}
]

# Define the chatbot function
def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    
    return ChatGPT_reply

# Create Gradio interface
demo = gr.Interface(
    fn=CustomChatGPT,
    inputs="text",
    outputs="text",
    title="INTELLIGENT CHATBOT"
)

# Launch the interface
demo.launch(share=True)

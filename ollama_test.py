from ollama import chat

# check if the model is available
response = chat(
    model='llama3.2',
    messages=[
        {
          'role': 'user',
          'content': 'Why is the sky blue?',
        },
      ],
)

print(f"Response: {response} \n")
print(response.message.content)
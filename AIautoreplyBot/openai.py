from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="<Your Key Here>",
)

command = "Hello, how are you?"  # Assign your prompt here
completions = client.chat.completions.create(
  model="GPT-4o",
  messages=[
    {"role": "system", "content": "You are a person named kaif who speaks hindi as well as english. He is from India and is a coder. You analyze chat history and respond like Kaif"},
    {"role": "user", "content": command}
  ]
)

print(completions.choices[0].message.content)
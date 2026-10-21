import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API KEY KAHA HAIN BHAI ")

client = Groq(api_key = my_api_key)

model = "openai/gpt-oss-20b"

role = "user"

prompt1 = " HI !"

prompt2 = " Excplain time travel in Detail in 100 words "

prompt3 = "Write a 1000 word edday on Machine Learning"

prompts = [prompt1 , prompt2 , prompt3]





for prompt in prompts:
    message = {
    "role" : role,
    "content" : prompt
    }
    messages = [ message]
    response = client.chat.completions.create(model = model , messages = messages )
    usage = response.usage
    print(f"Prompt: {prompt} --> your tokens: {usage.prompt_tokens} completion_tokens: {usage.completion_tokens} total tokens: {usage.total_tokens}")




 
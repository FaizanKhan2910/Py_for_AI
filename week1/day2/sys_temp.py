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

prompt = " SUggest a Name for my food company"


message_system = {
    "role" : "system",
    "content" : "You are My Brand Manger who suggest name for my food company  , name should be one word  , suggest only one"
}

message = {
    "role" : role,
    "content" : prompt
}

messages = [message_system, message]
#Temprature by default is meaing safe between 0 & 2 
#giving temprature is only alowed between 2 types 

response = client.chat.completions.create(model = model , messages = messages , temperature = 0)


print("#########################")

answer = response.choices[0].message.content

print(answer)


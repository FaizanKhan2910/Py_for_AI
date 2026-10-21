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
#struture it 
from pydantic import BaseModel
class Ticket(BaseModel):
    name: str
    email: str
    issue: str

schema = Ticket.model_json_schema()

response_format={
    "type" : "json_object",

}

system_prompt = f"""
Extract the personal Information from the ticket based in this schema and give in a json output.
{schema }
"""

message_system = {
    "role": "system",
    "content": system_prompt
}

text  = "hello My Name is Faizan Khan .yesterday i broke up wiht my girlfrnd. I Have an Iphone which is not working . and my hoe town is in Lucknow .My email is fhsd@gamil.com . " 

prompt = f"""
This is a Customer Ticket . Please extras  the personal information from this.
{text}
"""
message = {
    "role" : role,
    "content" : prompt
}


messages = [message_system, message]

response = client.chat.completions.create(model = model , messages = messages , response_format = response_format )


print("#########################")

answer = response.choices[0].message.content

print(json.dumps(json.loads(answer) , indent = 4))

# json pafhte kaisr hain

import json
raw_json = answer
data_file = json.loads(raw_json)
ticket = Ticket(**data)
print(ticket.name)
print(ticket.email)
print(ticket.issue)
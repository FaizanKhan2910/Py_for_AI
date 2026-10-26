
import os
import re
import time
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API KEY KAHA HAIN BHAI")

client = Groq(api_key=my_api_key)

model = "qwen/qwen3.8-27b"

message 
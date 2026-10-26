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


def llm_ans(prompt):
    message = {
        "role":"user",
        "content": prompt
    }

    message = [message]
    response = client.chat.completions.create(model = model , messages = message)
    ans = response.choices[0].message.content
    return ans

bad_prompt = """
#ROLE:
You are a support assitant at a mobile/laptop company
#TASK:
You have to classify the isssue in a catrgory
#CONSTRAINT
You have to classify the issue in one of the 3 categories namely billing , technical , return 
#OUTPUT FORMAT
Your answer should be in one word only. The one word should be one of the catrgories given in contraints
#EXAMPLE
FOR INSTANCE IF A USER COMPLAIN SAYS HE WANTS A REFUND THEN THE CATEGORY IS RETURN
#FALLBACK
IF THE ISSUE  IS UNRELATED TO ANY OF THE CATEGORIES MENTIONSED IN CONTRAINTS , THEN ANSWER SHOULD BE OTHER.
This is a user complaint:
MY LAPTOP FALL FROM CHAIR AND BREAK 
"""

print(llm_ans(bad_prompt))
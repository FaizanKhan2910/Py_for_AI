
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


# Tool 1: Get product price
def get_product_price(product):
    product = product.strip().lower()

    if product == "iphone 17":
        return 1000
    elif product == "iphone 15":
        return 500
    else:
        return 0


# Tool 2: Calculator
def calculator(expression):
    try:
        # Demo only: eval is unsafe for untrusted input.
        return eval(expression, {"__builtins__": {}}, {})
    except Exception:
        return "Calculator error!"


# Available tools
tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}


# System prompt
system_prompt = """
You are a ReAct agent.

You can use these tools:
1. get_product_price(product)
2. calculator(expression)

Follow this format exactly.

When you need a tool, respond with:
Thought: explain what you need
Action: tool_name("argument")

After receiving an Observation, continue reasoning.

When you have the final result, respond with:
Final Answer: your answer

IMPORTANT:
- Return Action as plain text, not as a native API tool call.
- Use only one Action per response.
- Do not invent tool results.
"""


def run_agent(question):

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    for step in range(5):

        print("\n---------------")
        print(f"Step {step + 1}")
        print("---------------")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
           
        )

        answer = response.choices[0].message.content

        if not answer:
            print("Model returned an empty response.")
            break

        print(answer)

        # Check for final answer
        if "Final Answer:" in answer:
            break

        # Find the Action
        match = re.search(
            r"Action:\s*(\w+)\((.*?)\)",
            answer,
            re.DOTALL
        )

        if match:
            tool_name = match.group(1)
            tool_input = match.group(2)

            tool_input = tool_input.strip()
            tool_input = tool_input.strip('"').strip("'")

            # Run the tool
            if tool_name in tools:

                result = tools[tool_name](tool_input)

                print(f"Observation: {result}")

                # Save assistant's response
                messages.append({
                    "role": "assistant",
                    "content": answer
                })

                # Send tool result back to the model
                messages.append({
                    "role": "user",
                    "content": f"Observation: {result}"
                })

            else:
                print(f"Tool not found: {tool_name}")
                break

        else:
            print("No Action found in response.")
            break

        # Wait 5 seconds between steps
        if step < 4:
            time.sleep(5)


# Test the agent
prompt = """
I have 5000 rupees.
What is the price of an iPhone 17?
How much money will I have left?
"""

run_agent(prompt)

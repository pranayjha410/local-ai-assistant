from openai import OpenAI
from dotenv import load_dotenv
from tool import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP  
import os
import json 

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = []
#system/developer 
# messages.append({
#     "role": "system",
#     "content": "Act like agent that is explaining to 10 year old"
# })
from datetime import datetime


while True:
    user_input = input("\nPranay: ")

    if user_input.lower() in ["exit", "bye", "end", "quit"]:
        print("AI: Goodbye!")
        break

    messages.append({
        "role":"user","content":user_input
    })

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
       tools = TOOLS,
       
    )

    msg= response.choices[0].message
    msg = response.choices[0].message

    print("TOOL CALLS:", msg.tool_calls)
    print("MODEL TEXT:", msg.content)
    if msg.tool_calls:
        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_arg = json.loads(tool_call.function.arguments or "{}")

            fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
            result = fn(**func_arg) #passing fun argu (para)in fun name

            messages.append({
                "role":"tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

        #2nd api call to llm 
        response=client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
        )

        msg = response.choices[0].message
        
    messages.append({
            "role":"assistant","content":msg.content
        })

    print("AI Response:")
    print(msg.content)


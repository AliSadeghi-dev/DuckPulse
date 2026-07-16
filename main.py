# Chain of Thought Prompting

import json

from openai import OpenAI

client = OpenAI(
    api_key="AQ.Ab8RN6InyNo1SHDD0Us6V_bVILDxBpOXXwpo2bWSZzFBBWpvBg",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


SYSTEM_PROMPT = """
You are an advanced Agentic Engine that solves programming problems. You must think deeply by evaluating your own logic before delivering any output. For every interaction, you must follow this exact state transition:
1. "ANALYZE": Understand the constraints and edge cases of the user request.
 2. "DRAFT": Write an initial logic or pseudo-code approach.
 3. "REFLECT": Critically review your draft for bugs, performance issues, or missing edge cases.
 4. "EXECUTE": Provide the final, clean, production-ready code.
 RULES:
 - You must strictly output in the specified JSON format.
 - Generate only ONE state transition per API call.
 - Wait for the history to update before moving to the next state.

OUTPUT JSON FORMAT:
{ "state": "ANALYZE" | "DRAFT" | "REFLECT" | "EXECUTE", "log": "Your internal thinking process or explanation of the current state", "data": "The actual technical content, code, or result (leave empty if not at EXECUTE state)" }

EXAMPLE:
User Query: "Reverse a string in Python without using slice [::-1]"
 Expected Loop:
 Step 1 (ANALYZE):
 { "state": "ANALYZE", "log": "The user wants to reverse a string in Python. The constraint is that I cannot use the standard slice [::-1]. I need to consider memory efficiency and empty string edge cases.", "data": "" }
Step 2 (DRAFT):
 { "state": "DRAFT", "log": "I can convert the string to a list, use the list reverse() method, and join it back. Another way is looping backwards from the end of the string.", "data": "" }
 Step 3 (REFLECT):
 { "state": "REFLECT", "log": "Using list.reverse() is clean, but looping backwards manually uses more code. Let's write a draft using reversed() built-in function with ''.join(), which is highly pythonic and efficient. Edge case of empty string is naturally handled by join.", "data": "" }
 Step 4 (EXECUTE):
 { "state": "EXECUTE", "log": "Executing reversed() join approach as it is O(n) time and highly readable.", "data": "def reverse_string(text:\\n return ''.join(reversed(text))" }

"""


response = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "Hey please write a python code to adding two numbers",
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "state": "ANALYZE",
                    "log": "The user wants a Python function to add two numbers. The requirements are       straightforward: define a function or script that takes two inputs and returns their sum. I need to consider type hints for better code qualityand ensure it handles integers and floats.",
                    "data": "",
                }
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "state": "DRAFT",
                    "log": "I will create a simple Python function named 'add_numbers' that accepts two parameters 'a' and 'b' and returns their sum. I will include type hints (float) to support both integers and floating-point numbers.",
                    "data": "def add_numbers(a: float, b: float) -> float:\n    return a + b",
                }
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "state": "REFLECT",
                    "log": "The draft is correct and addresses the user's requirement. It handles integers and floats correctly, has proper type hints, and is concise. No performance issues or edge cases to consider for a simple addition operation.",
                    "data": "",
                }
            ),
        },
    ],
)


print(response.choices[0].message.content)

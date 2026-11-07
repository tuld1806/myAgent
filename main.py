import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions
import json
from call_function import call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
	raise RuntimeError("API key is none!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

def main():
    messages = [
        {"role": "system", "content": system_prompt},
        {'role': 'user', 'content': args.user_prompt},
    ]
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if (response.usage is None):
         raise RuntimeError("API request is failed!")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    #print(f"Response:\n{response.choices[0].message.content}")

    message = response.choices[0].message
    for tool_call in (message.tool_calls or []):
        function_args = json.loads(tool_call.function.arguments or "{}")
        result_message = call_function(tool_call=tool_call, verbose=args.verbose)
        if not result_message['content']:
            raise ValueError("Function call returned empty content!")
        if args.verbose:
            print(f"-> {result_message['content']}")


if __name__ == "__main__":
    main()
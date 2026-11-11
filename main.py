import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions
import json
from call_function import call_function
import sys
from config import MAX_ITERS

total_prompt_tokens, total_response_tokens = 0, 0

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {'role': 'user', 'content': args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(MAX_ITERS):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print(f"Final response:\n{final_response}")
                print(f"Total prompt tokens: {total_prompt_tokens}")
                print(f"Total response tokens: {total_response_tokens}")
                return
        except Exception as e:
            print(f"Error in generate content: {e}")

    print(f'Maximum iterations ({MAX_ITERS} reached)')
    sys.exit(1)
    
def generate_content(client: OpenAI, messages: list, verbose: bool) -> str|None:
    global total_prompt_tokens, total_response_tokens

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    total_prompt_tokens += response.usage.prompt_tokens
    total_response_tokens += response.usage.completion_tokens
    if (response.usage is None):
        raise RuntimeError("API request is failed!")

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        return message.content

    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        result_message = call_function(tool_call=tool_call, verbose=verbose)
        if not result_message['content']:
            raise ValueError("Function call returned empty content!")
        messages.append(result_message)
        if verbose:
            print(f"-> {result_message['content']}")
    
    return None

if __name__ == "__main__":
    main()
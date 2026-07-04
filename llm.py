import os
import json
from groq import Groq

from dotenv import load_dotenv

load_dotenv()
api = os.getenv("GROQ_API_KEY")

from web import web_search
from file_handle import file_writer, file_reader, read_dir
from essentials import model_name, tools_schema, system_prompt
client = Groq(api_key=api)

print(f"Model Name: {model_name}")

tools = {
    "web_search": web_search,
    "file_writer": file_writer,
    "file_reader": file_reader,
    "read_dir": read_dir
}

def agent(user_prompt: str, session_id=None):
    global system_prompt, tools, tools_schema, model_name


    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    caller = True
    request_session = 1

    while caller:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools_schema,
            tool_choice="auto"
        )

        


        response_msg = response.choices[0].message

        usage = response.usage
        response_usage = {
            "Completion Tokens": usage.completion_tokens,
            "Prompt Tokeds": usage.prompt_tokens,
            "Total Tokens": usage.total_tokens,
            "Completion Time": usage.completion_time,
            "Completion Tokens Details": usage.completion_tokens_details,
            "Prompt Time": usage.prompt_time,
            "Prompt Tokens Details": usage.prompt_tokens_details,
            "Queue Time": usage.queue_time,
            "Total Time": usage.total_time,
        }

        if response_msg.tool_calls:
            tool_called = True
        else:
            tool_called = False

        assistant_message = {
            "role": response_msg.role,
            "content": response_msg.content or ""
        }

        if getattr(response_msg, "tool_calls", None):
            assistant_message["tool_calls"] = [
                {
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }
                for tool_call in response_msg.tool_calls
            ]


        messages.append(assistant_message)

        if response_msg.tool_calls:

            caller = True
            for tool_call in response_msg.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                exc_tool = tools.get(func_name)


                if exc_tool:
                    print(f"\n[Agent] Executing tool {func_name} with Arguments: {func_args}")
                    tool_output = exc_tool(**func_args)
                else:
                    tool_output = f"Tool '{func_name}' is not available."

                if not isinstance(tool_output, str):
                    tool_output = json.dumps(tool_output)


                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_output
                    }
                )
            request_session += 1
        else:
            caller = False
            agent_reply = response_msg.content
            


    print(messages)
    return agent_reply
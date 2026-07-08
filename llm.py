import os
import json
from groq import Groq
from get_time import get_time, get_day, get_year
from file_handle import file_writer, file_reader, read_dir
from essentials import model_name, tools_schema, system_prompt
from web import web_search
from dotenv import load_dotenv

load_dotenv()
api = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api)


tools = {
    "web_search": web_search,
    "file_writer": file_writer,
    "file_reader": file_reader,
    "read_dir": read_dir,
}


def agent(user_prompt: str, chat_id=None):

    chat_data = {
        "_id": chat_id,
        "User Input": user_prompt,
        "Agent Output": None,
        "Date & Time": {"Time": get_time(), "Day": get_day(), "Year": get_year()},
        "Usage": {"Total Tokens": 0, "Input Tokens": 0, "Output Tokens": 0},
    }

    request_process = []

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    caller = True
    while caller:
        response = client.chat.completions.create(
            model=model_name, messages=messages, tools=tools_schema, tool_choice="auto"
        )

        print("Requested to Model")

        response_msg = response.choices[0].message

        usage = response.usage
        response_usage = {
            "Completion Tokens": usage.completion_tokens,
            "Prompt Tokens": usage.prompt_tokens,
            "Total Tokens": usage.total_tokens,
        }

        assistant_message = {
            "role": response_msg.role,
            "content": response_msg.content or "",
        }

        if getattr(response_msg, "tool_calls", None):
            assistant_message["tool_calls"] = [
                {
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in response_msg.tool_calls
            ]

        messages.append(assistant_message)

        tools_called = []
        if response_msg.tool_calls:
            print("Tools Calling")
            caller = True
            for tool_call in response_msg.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                exc_tool = tools.get(func_name)

                if exc_tool:
                    print(
                        f"\n[Agent] Executing tool {func_name} with Arguments: {func_args}"
                    )
                    tool_output = exc_tool(**func_args)
                else:
                    tool_output = f"Tool '{func_name}' is not available."

                if not isinstance(tool_output, str):
                    tool_output = json.dumps(tool_output)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_output,
                    }
                )
                tools_called.append(
                    {
                        "Tool Call ID": tool_call.id,
                        "Funtion Name": func_name,
                        "Function Arguments": func_args,
                        "Output": tool_output,
                    }
                )

        else:
            caller = False
            agent_reply = response_msg.content

        request_process.append(
            {"Tokens Usage": response_usage, "Tools Called": tools_called}
        )

        chat_data["Request Process"] = request_process
        chat_data["Usage"]["Total Tokens"] += usage.total_tokens
        chat_data["Usage"]["Input Tokens"] += usage.prompt_tokens
        chat_data["Usage"]["Output Tokens"] += usage.completion_tokens

    chat_data["Agent Output"] = agent_reply

    return agent_reply, chat_data

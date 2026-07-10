model_name = "meta-llama/llama-4-scout-17b-16e-instruct"

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Searches the web for the given query and returns a text summary of results",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query formulation"
                    },
                    "max_results": {
                        "type": "string",
                        "description": "The maximum number of search results to return"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "file_writer",
            "description": "Writes file by Given file content, and named the file by given file name and file extension",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "Name of the file. User will provide if not then LLM will provide based on the context."
                    },
                    "file_ext": {
                        "type": "string",
                        "description": "Extention of the generated file. LLM will provide based on User's prompt"
                    },
                    "file_content": {
                        "type": "string",
                        "description": "Content of the file. Thesea the data that will be contained in the generated file."
                    }
                },
                "required": ["file_name", "file_ext", "file_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "file_reader",
            "description": "Reads a specific file and If a file doesn't exist then return a error message.",
            "parameters": {
                "type": "object",
                "properties":{
                    "file_name": {
                        "type": "string",
                        "description": "Name of the file that will be read."
                    }
                },
                "required": ["file_name"]
            }
        }
    },
    
    {
        "type": "function",
        "function": {
            "name": "read_dir",
            "description": "Gets a list of all the files in the dir. No parameters needed",
            "parameters": {
                "type": "object",
                "properties":{
                    "file_name": {
                        "type": "string",
                        "description": "Any thing will be okhay"
                    }
                },
                "required": []
            }
        }
    }
]

system_prompt = """You are a helpful AI assistant with access to the following functions:

1. web_search - Search the web for information
2. file_writer - Write content to a file
3. file_reader - Read content from a file
4. read_dir - List files in a directory

Instructions:
- Use these functions to complete user requests when appropriate
- Only call functions that match the user's needs
- Provide clear responses about what you're doing
- If a function call fails, explain the error and suggest alternatives
- Always be helpful and professional"""
from llm import agent, model_name
from chat_session import exsiting_session, get_chat_id, new_session, update_session

print("Welcome to ASCLI AI Agent")
print("Model Name:", model_name)
print("Continue with Existing Session or Crete a new session")
print()
while True:
    res = input("Enter; [1]: Existing Session\n[2]: New Session.\nAnswer: ")
    if res == "1":
        respns = exsiting_session()
        session = respns[0]
        print("Retrived Existing Sessiion.")
        print("Session ID:", session)
        print("Tokens Usage:", respns[2])
        print("Last Used:", respns[1])

        chat_id = get_chat_id(session)

        break

    elif res == "2":
        print("=" * 30)
        session = new_session()
        print("New Session Created.\nSession No:", session)

        chat_id = 1
        break

    else:
        print("Entered a Wrong Value")
        continue


while True:
    print("Enter your question or enter [exit] to quit.")

    quns = input("==> Question: ")

    if quns.lower() == "exit":
        print("!!!! Exiting the Program....")
        break

    print()
    print("##############")
    print("AGENT: CHAT Id", chat_id)
    print("##############\n")

    ans, chat = agent(user_prompt=quns, chat_id=chat_id)

    update_session(chat, session)

    print("\n===AGENT FINAL REPLY===\n", ans)
    chat_id += 1

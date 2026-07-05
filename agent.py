from llm import agent
from chat_session import new_sessio

while True:
    pr

    print()
    print("=" * 30)

    print("Enter your question or enter [exit] to quit.")

    quns = input("==> Question: ")

    if quns.lower() == "exit":
        print("!!!! Exiting the Program....")
        break
    print()
    print("##############")
    print("AGENT: CHAT SESSION")
    print("##############\n")

    ans = agent(user_prompt=quns)
    print("\n===AGENT FINAL REPLY===\n", ans)

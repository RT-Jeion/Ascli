from llm import agent
from chat_session import chat_session

while True:
    print()
    print("="*30)


    print("Enter your question or enter [exit] to quit.")

    quns = input("==> Question: ")
    
    if quns.lower() == "exit":
        print("!!!! Exiting the Program....")
        break
    
    print()
    print("##############")
    print("AGENT: CHAT SESSION", chat)
    print("##############\n")

    ans = agent(user_prompt=quns)
    print("===AGENT FINAL REPLY===\n",ans)
    


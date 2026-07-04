class ChatSessionNumberExceeded(Exception):
    """Raised when a user tries to withdraw more money than they have."""
    pass


from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = ["Ascli"]

chat_sessions = db['Sessions']


def chat_session() -> int:
    import json
    import random
    try:
        with open("chat_session.json", "r") as f:
            chats = json.load(f)
    except:
        chats = []
        print(chats)
    try:
        while True:
            new_chat = random.randint(10000000,999999999)
            if new_chat not in chats:
                chats.append(new_chat)
                break
            raise ChatSessionNumberExceeded("Chat session number exceeded in 8 digit value")

        with open("chat_session.json", 'w') as f:
            json.dump(chats, f)

            return new_chat
    except ChatSessionNumberExceeded as e:
        print(e)
    except Exception as e:
        print("Error found:", e)

if __name__=="__main__":
    chat = chat_session()
    print(chat)
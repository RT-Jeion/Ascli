class ChatSessionNumberExceeded(Exception):
    """Raised when a user tries to withdraw more money than they have."""

    pass


def new_session():
    import random
    from pymongo import MongoClient

    client = MongoClient("mongodb://localhost:27017/")
    db = client["Ascli"]

    sessions = db["Sessions"]

    sessions_id = sessions.find({}, {"_id": 1})
    sessions_id = [i["_id"] for i in list(sessions_id)]

    try:
        while True:
            new_session = random.randint(10000000, 99999999)
            if new_session not in sessions_id:
                print("New session:", new_session)

                sessions.insert_one({"_id": new_session})

                break
            raise ChatSessionNumberExceeded(
                "Chat session number exceeded in 8 digit value"
            )

        return new_session

    except ChatSessionNumberExceeded as e:
        print(e)
    except Exception as e:
        print("Error found:", e)


if __name__ == "__main__":
    chat = new_session()

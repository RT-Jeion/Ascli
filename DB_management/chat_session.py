from pymongo import MongoClient
import random
from Utils.get_time import get_time, get_day, get_year

from datetime import datetime

now_time = datetime.now()

client = MongoClient("mongodb://localhost:27017/")
db = client["Ascli"]


def new_session():
    sessions = db["Sessions"]

    sessions_id = sessions.find({}, {"_id": 1})
    sessions_id = [i["_id"] for i in list(sessions_id)]

    while True:
        new_session = random.randint(10000000, 99999999)
        if new_session not in sessions_id:
            print("New session:", new_session)
            sessions.insert_one(
                {
                    "_id": new_session,
                    "Created": {
                        "Time": get_time(),
                        "Day": get_day(),
                        "Year": get_year(),
                    },
                    "Usage": {"Total_Tokens": 0, "Input_Tokens": 0, "Output_Tokens": 0},
                }
            )
            break
    return new_session


def update_session(chat, session_id):

    print("[DB]: Chat Has Been Updating of Session:", session_id)

    session_db = db[f"Session: {session_id}"]
    sessions = db["Sessions"]

    chat_tokens = chat["Usage"]
    total_tokens = chat_tokens["Total Tokens"]
    input_tokens = chat_tokens["Input Tokens"]
    output_tokens = chat_tokens["Output Tokens"]

    session_db.insert_one(chat)

    sessions.update_one({"_id": session_id}, {"$set": {"Last Used": now_time}})

    sessions.update_one(
        {"_id": session_id},
        {
            "$inc": {
                "Usage.Total_Tokens": total_tokens,
                "Usage.Input_Tokens": input_tokens,
                "Usage.Output_Tokens": output_tokens,
            }
        },
    )

    print("[DB]: Chat Has been Updated")


def exsiting_session():
    sessions = db["Sessions"]

    sorting = -1
    limit = 5

    while True:
        num = 1
        choices = dict()
        print("[DB]: Showing Last 5 session.")
        for session in sessions.find().sort("Last Used", sorting):
            id = session["_id"]
            last_used = session["Last Used"]
            tokens_usage = session["Usage"]
            tokens_usage = f"Tokens Usage:, Total: {tokens_usage['Total_Tokens']}, Input: {tokens_usage['Input_Tokens']}, Output: {tokens_usage['Output_Tokens']}"

            choices[num] = [id, last_used, tokens_usage]

            print("\nSessions number:", num)
            print("Session ID:", id)
            print("--------------------------")
            print("Last Used:", last_used)
            print(tokens_usage)
            print("---------------------------")
            num += 1
            if limit:
                if num > limit:
                    break

        print(
            "\nEnter session number to Continue.\nOr Enter [0] to show all sessions.\nOr Enter [-1] to show old 5 sessions"
        )

        res = int(input("==>"))
        if res == 0:
            limit = None
            continue
        elif res == -1:
            sorting = 1
            continue
        else:
            break

    return choices[res]


def get_chat_id(session_id):
    session_id = f"Session: {session_id}"
    session = db[session_id]

    chat_ids = session.find({}, {"_id": 1})
    chat_ids = [i["_id"] for i in list(chat_ids)]
    if not chat_ids:
        chat_id = 1
    else:
        chat_id = chat_ids[-1] + 1

    return chat_id


if __name__ == "__main__":
    get_chat_id(46754127)

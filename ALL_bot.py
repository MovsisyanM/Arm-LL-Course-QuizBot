import TelegramBot
import pandas as pd
from notifier import notify
import json
from pathlib import Path

# region proc


fwd = [[">>"]]
env = Path(".env")
remove = "remove"


def ProcessMsg(user_id, message, states):

    if user_id not in states.keys() or "m0" not in states[user_id].keys():
        states[user_id] = {}
        states[user_id]["m0"] = True
        return states, illustrations["0"], fwd

    keys = states[user_id].keys()

    with open(env / "reset_key") as rk:
        if message == "reset: " + rk.read():
            states[user_id] = {}
            return states, f"Progress reset for {user_id}", fwd

    m = 0

    if message == ">>" and f"m{m}" not in keys and f"m{m-1}" in keys:
        states[user_id][f"m{m}"] = True
        return states, "The moon illuminated the mountainous path for Sis and flew off.", fwd

    return states, "Don't stray from your destiny..." if f"m{m-1}" not in keys else "...", None


def state_sync(user_id, message, engine):
    df = pd.read_sql_query(
        f"select * from allQuizBot_states where uid = {user_id}", engine)
    states = {}

    for i, row in df.iterrows():
        states[user_id] = json.loads(row["state"])

    states, a, b = ProcessMsg(user_id, message, states)

    if len(df) == 0:
        engine.execute(
            f"INSERT INTO `allQuizBot_states`(`uid`, `state`) VALUES ({user_id}, '{json.dumps(states[user_id])}')")
    else:
        engine.execute(
            f"UPDATE `allQuizBot_states` SET `state`='{json.dumps(states[user_id])}' WHERE uid = {user_id}")

    return a, b


# endregion proc

with open(env / "toekn", "r") as tkn:
    quizbot = TelegramBot.Bot(
        r"https://api.telegram.org/bot" + tkn.read().strip())


def processALLQuizBotMsg(data, engine):
    """Processes incoming messages"""

    def respond(message, engine):

        chat = message["message"]["chat"]
        sender = chat["id"]
        content = str(message["message"]["text"]
                      ) if "text" in message["message"] else ""
        name = ["first_name"] if "first_name" in chat.keys() else None

        # region state sync & response

        # preventing sql injections
        for ch in ("qwertyuioplkjhgfdsazxcvbnm;'`[]()" + '"'):
            if ch in content:
                notify(f"Prevented possible misuse: {content}")
                content = "Լատինատառ գրություն"
                break

        try:
            engine.execute(
                "INSERT INTO allQuizBot_msges (sender, name, content) VALUES (%s, %s, %s)", (sender, name, content))
        except Exception as e:
            notify(f"Failed to log ArmenianLL QuizBot\n{str(e)}")

        answer, reply = state_sync(sender, content, engine)

        if reply == remove:
            reply_ = quizbot.RemoveKeyboardMarkup()
            quizbot.send_message(sender, answer, reply_)
            return
        elif reply is None:
            reply_ = None
        else:
            reply_ = quizbot.ReplyKeyboardMarkup(reply, False, False, False)

        if answer in illustrations.values():
            answer_ = illustration_links[answer]
            quizbot.send_photo(sender, answer_, None, False, reply_)
            return
        else:
            quizbot.send_message(sender, answer, reply_)

    # region discretizing incoming requests

    if isinstance(data, list):
        for i in data:
            try:
                respond(i, engine)
            except Exception as e:
                notify(f"Failed to respond MountainousBot\n{i}\n{str(e)}")
    else:
        try:
            respond(data, engine)
        except Exception as e:
            notify(f"Failed to respond MountainousBot\na{data}\n{str(e)}")

    # endregion discretizing incoming requests

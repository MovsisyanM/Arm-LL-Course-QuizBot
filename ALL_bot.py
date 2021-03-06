import TelegramBot
import pandas as pd
from notifier import notify
import json
from pathlib import Path

# region proc


fwd = [["Օկ"]]
env = Path(".env")
remove = "remove"

replies = {
    0: ("Ողջույն, բարի գալուստ։ Այս բոտը կթարմացնի հիշողությունդ` ամփոփելով այս կիսամյակը։", fwd, (0, 0)),

    1: ("Լրացրեք ____-ը", fwd, (0, 0)),
    2: ("Բուքը, երգը, ____",                             [["մայրը", "գիրքը"], ["երեխան", "փոքրիկը"]], (1, 0)),
    3: ("Գառ ____",                                     [["ախպերիկ", "ապերիկ"], ["ախպեր", "ախպոր"]], (0, 0)),
    4: ("____ փուչ ընկույզների մասին",                   [["Հեքիաթ", "Առակ"], ["Պատմվածք", "Վեպ"]], (0, 0)),
    5: ("____մեքենան",                                  [["Ավտո", "Գրա"], ["Կարի", "Թանկ"]], (0, 1)),
    6: ("ARM____",                                       [["ageddon", "Comedy"], ["News", "Donmag"]], (0, 0)),
    7: ("Հողի ____",                                     [["Գույնը", "Ցանքը"], ["Բույրը", "Դողը "]], (1, 1)),
    8: ("էդ ____",                                       [["Օրը", "Գիշեր"], ["Երեկո", "Պահին"]], (0, 1)),
    9: ("____ շշեր",                                     [["Դատարկ", "Հայելապատ"], ["Թափանցիկ", "Կոտրված"]], (1, 0)),
    10: ("Երրերդ ... ____",                             [["Մաս", "Մասիվ"], ["Կանգառ", "Կայարան"]], (0, 0)),

    10: ("Գուշակիր գրողին ըստ կարճ սյուժեի", fwd, (0, 0)),
    11: ("Արևածաղիկ չրթելու նման գյուղեր են գրավում",   [["Քիրվա", "Հողի դողը"], ["Ալիբի", "Գիր-ղուշ"]], (0, 1)),
    12: ("Ծեր մարդու հիշողության տեր երիտասարդ",      [["Ալիբի", "Գրամեքենան"], ["Հեքիաթ փուչ  ընկույզների մասին", "էդ գիշեր"]], (0, 0)),
    13: ("Էակ զուրկ է-ից",                              [["Վերջը", "Հողի դողը"], ["Ալիբի", "Գրամեքենան"]], (1, 1)),
    14: ("Ձրիակեր սովետական տեսանկյունից",            [["Գիր-ղուշ", "Վագոնից թռչելու ժամանակը"], ["Տժվժիկ", "Քիրվա"]], (1, 0)),
    15: ("Սառած դպրոցական",                           [["Բուք, երգը, երեխան", "Անմոռանալի սովետ"], ["էդ գիշեր", "Երրորդ…մաս"]], (0, 0)),
    16: ("Կապիտալիզմ vs արվեստ",                      [["Երրորդ…մաս", "Անմոռանալի սովետ"], ["Վագոնից թռչելու ժամանակը", "Վերջը"]], (1, 0)),
    17: ("Ճանապարհորդություն երթուղայինով",            [["Վագոնից թռչելու ժամանակը", "Ալիբի"], ["ARMageddon", "Երրորդ․․․ մաս"]], (1, 1)),
    18: ("Մահ շատ հարմարությունից",                    [["Գառ-ախպերիկ", "Բուք, երգը, երեխան"], ["Վագոնից թռչելու ժամանակը", "Ալիբի"]], (0, 0)),
    19: ("Երեխային և կնոջը վաղաժամ լքում է",           [["Հեքիաթ փուչ ընկույզների մասին", "Վերջը"], ["Սկյութների ստվերները", "Գառ-ախպերիկ"]], (0, 1)),
    20: ("Հավեսի միկրոէկոնոմիկա",                       [["Հեքիաթ փուչ ընկույզների մասին", "Քիրվա"], ["Երրորդ․․․ մաս", "Ալիբի"]], (0, 0)),
    21: ("Կովի փողը բգին կանգնեց",                      [["ARMageddon", "Ալիբի"], ["Հողի դողը", "Քիրվա"]], (1, 1)),
    22: ("Կռիվ-կռիվ",                                   [["Գիր-ղուշ", "Բուք, երգը, երեխան"], ["ARMageddon", "Վերջը"]], (1, 0)),
    23: ("Կաշառակեր խնամակալը",                       [["Թափանցիկ շշեր", "Ալիբի"], ["Էդ գիշերը", "ARMageddon"]], (0, 0)),
    24: ("Վախում եմ Յաշշիկով վրաերթի ենթարկեն ինձ",   [["Գուշակություն հայելիներով", "Նկուղը"], ["Թափանցիկ շշեր", "Երրորդ…մաս"]], (0, 1)),
    25: ("Ամոթ բան",                                    [["Սրբիչը", "Անմոռանալի սովետ"], ["Նկուղը", "Անսովոր գիշեր"]], (0, 0)),

    26: ("Հարցեր պրեզենտացիաներից",                                             fwd, (0, 0)),
    27: ("Որն է Երևանի ամենաերկար փողոցը",                                      [["Արշակունյաց", "Մյասնիկյան"], ["Մաշտոցի", "Բաղրամյան"]], (0, 0)),
    28: ("Որ թաղամասում են մինչև հիմա օգտագործում հանրային բաղնիք",             [["Երրորդ մաս", "Կոնդ"], ["Բանգլադեշ", "Փոքր կենտրոն"]], (0, 1)),
    29: ("Ներկայումս ում անունն է կրում Մալիբու այգին",                             [["Տիգրան Մեծ", "Աբգար հինգերորդ"], ["Դիանա Աբգար", "Հայկ Մարության"]], (1, 0)),
    30: ("Որտե՞ղ է գտնվում Բերքաբերը",                                             [["Վայոց ձորի մարզ", "Կոտայքի մարզ"], ["Գեղարքունիքի մարզ", "Տավուշի մարզ"]], (1, 1)),
    31: ("Ո՞ր համալսարանն են ավարտել Ռոբերտ Քոչարյանը և Կարեն Դեմիրճյանը",      [["ԵՊՀ"], ["Գյուղինստիտուտ"], ["Պոլիտեխնիկական համալսարան"], ["Ամերիկյան համալսարան"]], (2, 0)),
    32: ("Կողբի բարբառով ինչ է նշանակում «Քաղաք դաստու»",                         [["Քաղաքի ուսուցիչ", "Քաղաքային"], ["Քաղաքացի", "Քաղաքամետ"]], (1, 1)),
    33: ("Որտեղ է գտնվում «Տղան և ինքնաթիռները» հայտնի գրաֆիտին:",               [["Մյասնիկյան", "Աբովյան"], ["Մաշտոցի", "Արամի"]], (0, 0)),
    34: ("Երևանը ունեցել է ճոպանողի, որն օգտագործվել է մինչև 2004 թվական",         [["Ճիշտ է", "Սխալ է"]], (0, 0)),
    35: ("Շնորհակալություն, հաջողություն",         [["խնդրեմ, հաջողություն"]], (0, 0)),
}

with open(env / "reset_key") as rk:
    reset_key = rk.read()


def ProcessMsg(user_id, message, states):

    if user_id not in states.keys() or "0" not in states[user_id].keys():
        states[user_id] = {}
        states[user_id][0] = True
        return states, replies[0][0], replies[0][1]

    keys = states[user_id].keys()

    if message == "reset: " + reset_key:
        states[user_id] = {}
        return states, f"Նորից սկսենք, {user_id}", fwd

    for i in range(1, len(replies)):
        # find the progress that the user has made
        if str(i) not in keys and str(i-1) in keys:
            # if the user wrote the correct answer
            if message.lower().strip() == replies[i-1][1][replies[i-1][2][0]][replies[i-1][2][1]].lower().strip():
                # progress
                states[user_id][i] = True
                # return the next question
                return states, replies[i][0], replies[i][1]
            # else try again
            return states, "Կրկին փորձիր, պատասխանդ սխալ էր։\n" + replies[i-1][0], replies[i-1][1]

    return states, "...", None


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

with open(env / "token", "r") as tkn:
    quizbot = TelegramBot.Bot(
        f"https://api.telegram.org/bot{tkn.read().strip()}/")


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
        for ch in (";'`[]()" + '"'):
            if ch in content:
                notify(f"Prevented possible misuse: {content}")
                content = "Անկապ գրություն"
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

        quizbot.send_message(sender, answer, reply_)

    # region discretizing incoming requests

    if isinstance(data, list):
        for i in data:
            try:
                respond(i, engine)
            except Exception as e:
                notify(f"Failed to respond ALL_bot\n{i}\n{str(e)}")
    else:
        try:
            respond(data, engine)
        except Exception as e:
            notify(f"Failed to respond ALL_bot\na{data}\n{str(e)}")

    # endregion discretizing incoming requests

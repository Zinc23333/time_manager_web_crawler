import datetime as dt
import threading
from typing import Any
from supabase import create_client, Client
from env import SUPA_URL, SUPA_ANON
from const import prompt_relevance
from ai import askAi

supa: Client = create_client(SUPA_URL, SUPA_ANON)  # type: ignore

def assess_relevance(ctask_id: int, user_id: int, msg: str) -> None:
    r4 = askAi(msg, prompt_relevance)
    try:
        if r4:
            relvance = int(r4)
        else:
            relvance = -1
    except Exception as e:
        print("ERR:", e)
        relvance = -1

    if 0 <= relvance <= 5:
        supa.table("relevance_of_ctask_and_user").insert({
            "ctaskId": ctask_id,
            "userId": user_id,
            "relevance": relvance,
        }).execute()

if __name__ == "__main__":
    r1 = supa.table("user_prompts").select("userId, prompt").execute()
    r2 = supa.table("crawler_tasks").select("id, tasks").execute()
    r3 = supa.table("relevance_of_ctask_and_user").select("ctaskId, userId").execute()

    tus = [(tu["ctaskId"], tu["userId"]) for tu in r3.data]
    ths = []

    for u in r1.data:
        for w in r2.data:
            if (w["id"], u["userId"]) in tus:
                continue

            ts = [f"{i+1}. {t["title"]}\n{t["summary"]}" for i, t in enumerate(w['tasks'])]
            m = f"事件:\n{"\n".join(ts)}\n\n\n\n用户信息:\n{u["prompt"]}"

            ths.append(threading.Thread(target=assess_relevance, args=(w["id"], u["userId"], m)))
    
    for th in ths:
        th.start()

import datetime as dt
from typing import Any
from dotenv import load_dotenv
from supabase import create_client, Client
from random import randint
import os

load_dotenv()

url: str = os.environ.get("SUPA_URL") # type: ignore
key: str = os.environ.get("SUPA_ANON") # type: ignore
supa: Client = create_client(url, key)


def get_newest_code() -> bool:
    try:
        r = supa.table("crawler_web").select("id, pythonCode").execute()
        for d in r.data:
            with open(f"temp_code/n{d["id"]}.py", "w") as f:
                f.write(d["pythonCode"])
        return True
    except:
        return False
    
def upload_news(web_id: int, url: str, tasks: list[dict[str, Any]]):
    supa.table("crawler_tasks").upsert({"webId": web_id, "url": url, "tasks": tasks}, on_conflict="url").execute()

def get_handled_urls() -> list[str]:
    r = supa.table("crawler_tasks").select("url").execute()
    return [d["url"] for d in r.data]

def update_time(web_id: int):
    supa.table("crawler_web").update({"lastCrawl": dt.datetime.now().astimezone().isoformat()}).eq("id", web_id).execute()

if __name__ == "__main__":
    update_time(1)
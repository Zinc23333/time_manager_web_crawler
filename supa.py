import datetime as dt
from typing import Any
from supabase import create_client, Client
from env import SUPA_URL, SUPA_ANON

supa: Client = create_client(SUPA_URL, SUPA_ANON)  # type: ignore

def get_newest_code() -> bool:
    try:
        r = supa.table("crawler_web").select("id, pythonCode").eq("verify", True).execute()
        for d in r.data:
            with open(f"temp_code/n{d["id"]}.py", "w") as f:
                f.write(d["pythonCode"])
        return True
    except:
        return False
    
def upload_news(web_id: int, url: str, tasks: list[dict[str, Any]], mindmap: str | None, title: str):
    supa.table("crawler_tasks").upsert({"webId": web_id, "url": url, "tasks": tasks, "mindmap": mindmap, "title": title}, on_conflict="url").execute()

def get_handled_urls() -> list[str]:
    r = supa.table("crawler_tasks").select("url").execute()
    return [d["url"] for d in r.data]

def update_time(web_id: int):
    supa.table("crawler_web").update({"lastCrawl": dt.datetime.now().astimezone().isoformat()}).eq("id", web_id).execute()

if __name__ == "__main__":
    update_time(1)
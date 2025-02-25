# ===
from fake_crawler_code import get_news_list, get_news
web_id = 0
# ===

import ai, supa
def handle_news(handled: list[str]) -> None:
    urls = get_news_list()
    for url in urls:
        if url not in handled:
            try:
                news = get_news(url)
                
                r = ai.recognize(news)
                if not r:
                    continue
                
                l = ai.parseForDb(r, news)
                if not l:
                    continue
                
                supa.upload_news(web_id, url, l)
            except:
                ...
                
    


if __name__ == "__main__":
    handled = supa.get_handled_urls()
    handle_news(handled)
    supa.update_time(web_id)

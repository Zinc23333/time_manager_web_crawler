from typing import Any
from openai import OpenAI
from json import loads
import const
from diskcache import Cache  # type: ignore
from env import DS_KEY

client = OpenAI(
    api_key = DS_KEY,
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

cache = Cache(".caches/ai")

# 0: 正在询问ai

# def recognizeForUser(msg: str) -> str:

def askAi(msg: str, prompt=const.prompt_basic) -> str|None:
    print(f"SEND: {msg}")
    response = client.chat.completions.create(
        model="deepseek-v3",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": msg},
        ],
        stream=False
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content
def recognize(msg: str) -> list[dict[str, Any]] | None:
    c = cache.get(msg)
    if c:
        return c

    try:
        r = askAi(msg)
        # print(f"SEND: {msg}")
        # response = client.chat.completions.create(
        #     model="deepseek-v3",
        #     messages=[
        #         {"role": "system", "content": const.prompt_basic},
        #         {"role": "user", "content": msg},
        #     ],
        #     stream=False
        # )

        # print(r)
        
        content = "".join([c for c in r.split() if "```" not in c]).strip()  # type: ignore
        j: list[dict[str, Any]] = loads(content)  # type: ignore
        cache.set(msg, j)
        return j

        # return r
    except Exception as e:
        print("ERR: ", e)
        return None

def convertToMindmap(msg: str) -> str | None:
    try:
        response = client.chat.completions.create(
            model="deepseek-v3",
            messages=[
                {"role": "system", "content": const.prompt_mindmap},
                {"role": "user", "content": msg},
            ],
            stream=False
        )
        content = response.choices[0].message.content
        if content is None:
            return None

        for line in content.split("\n"):
            l = line.lstrip()
            if l and l.startswith("- ") is False:
                return None
        return content
    
    except Exception as e:
        return None
        

# 解析：用于数据库
# param j: 输入json
# param c: 输入原文
def parseEventForDb(j: dict[str, Any], c: str) -> dict[str, Any]:
    j["startTime"] = j["startTime"] * 1000 if j["startTime"] else None
    j["endTime"] = j["endTime"] * 1000 if j["endTime"] else None
    j["content"] = c
    j["source"] = "网页爬取"
    
    return j

# 该方法会修改原始数据
def parseForDb(l: list[dict[str, Any]], c: str) -> list[dict[str, Any]]:
    return [parseEventForDb(j, c) for j in l]


if __name__ == "__main__":
    print(recognize("请通知退役大学生士兵（含转本）、军转生（含转本）持大学生士兵退役证等相关证件于2025年1月7日-2025年1月10前至东苑服务大厅7号窗口办理2024-2025学年第一学期体育免修，谢谢！遵循自愿原则，办理免修的体育课程成绩记70分。"))
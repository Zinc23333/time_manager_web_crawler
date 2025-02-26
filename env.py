SUPA_URL, SUPA_ANON, DS_KEY = "", "", ""

with open(".env", "r") as f:
    for l in f.readlines():
        if l.startswith("SUPA_URL"):
            SUPA_URL = l.split("=")[1].strip()
        elif l.startswith("SUPA_ANON"):
            SUPA_ANON = l.split("=")[1].strip()
        elif l.startswith("DS_KEY"):
            DS_KEY = l.split("=")[1].strip()
from supa import get_newest_code
import os, shutil

if __name__ == "__main__":
    if os.path.exists("temp_code"):
        shutil.rmtree("temp_code")    
    os.mkdir("temp_code")
    
    if not get_newest_code():
        exit()
    

    with open("crawler.py", "r") as f:
        template_code = f.readlines()

    for file in os.listdir("temp_code"):
        no = file[1:-3]
        template_code[1] = f"from temp_code.n{no} import get_news_list, get_news\n"
        template_code[2] = f"web_id = {no}\n"

        with open(f"gen-{no}.py", "w") as f:
            f.writelines(template_code)
        os.system(f"python gen-{no}.py")

        os.remove(f"gen-{no}.py")
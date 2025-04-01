import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, parse_qs
import subprocess
import config


def get_clean_appid_from_workshop(workshop_id):
    
    # 1. 获取创意工坊页面
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={workshop_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    # 2. 解析游戏链接
    soup = BeautifulSoup(response.text, "html.parser")
    game_link = soup.find("a", href=re.compile(r"store\.steampowered\.com/app/\d+"))
    if not game_link:
        return None

    # 3. 提取纯 AppID（去掉 ?snr=...）
    app_url = game_link["href"]
    appid = re.search(r"/app/(\d+)", app_url).group(1)
    return appid


def extract_workshop_id(url):
    """
    从 Steam 创意工坊 URL 提取 id 参数。
    示例:
        >>> extract_workshop_id("https://steamcommunity.com/sharedfiles/filedetails/?id=3383078008")
        3383078008
    """
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    workshop_id = params.get("id", [None])[0]
    return int(workshop_id) if workshop_id else None




def run_steamcmd(app_id, workshop_id):
    from commands import windowstoast
    print(f"开始下载：{app_id} - {workshop_id}")
    windowstoast(config.appname, f'⚠️开始下载 游戏id: {app_id} 创意工坊id:{workshop_id}\n*下载完成前关闭程序将下载失败*',2)

    cmd = [config.steamcmd_path+"steamcmd.exe","+login", "anonymous","+workshop_download_item", str(app_id), str(workshop_id),"+quit"]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1,encoding="utf-8")

    success = False
    error = False

    while True:
        # 读取一行 stdout
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            #print(output.strip())  # 实时打印

            # 检测成功或失败
            if "Success. Downloaded item" in output:
                success = True
            elif "ERROR! Download item" in output:
                error = True
                error_message = output[output.find("ERROR!"):output.find(".")+len(".")]

    # 检查返回值
    return_code = process.poll()
    if return_code != 0 or error:
        print(f"❌ {error_message}")
        windowstoast(config.appname, '❌下载失败：\n{error_message}',2)

        return False
    elif success:
        print("✅ 下载成功！")
        windowstoast(config.appname, f"✅ 创意工坊物品: {workshop_id} 下载成功！",2)

        return True


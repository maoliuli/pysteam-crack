import os
import jsontoon
import configparser
import subprocess
import config

# 获取当前工作目录
exe_path = os.getcwd()
print(f"Debug: 当前工作目录为 {exe_path}")


def startGame(appid):
    gameconfig = jsontoon.JSONConfig(config.gameconfig_path)
    
    game = gameconfig.read(appid)
    print(f"Debug: 读取到的游戏数据为 {game}")
    #写入启动器配置文件
    config1 = configparser.ConfigParser()
    
    config1['SteamClient'] = {
        'Exe': game["path"],
        'ExeRunDir': os.path.dirname(game["path"]),
        'ExeCommandLine': game["arguments"],
        'AppId': appid,
        'SteamClientDll':'steamclient.dll',
        'SteamClient64Dll':'steamclient64.dll'
    }
    config2_path = os.path.join(exe_path, "backend","lib","GoldbergSteamEmu", 'steam_settings')
    if game["disable_overlay"]:
        jsontoon.write_txt(config2_path+"//disable_overlay.txt", config1)
    else:
        if  os.path.exists(config2_path+"//disable_overlay.txt") :
            os.remove(config2_path+"//disable_overlay.txt")

    if game["offline_mode"]:
        jsontoon.write_txt(config2_path+"//offline.txt", config1)
    else:
        if os.path.exists(config2_path+"//offline.txt") :
            os.remove(config2_path+"//offline.txt")

    config_file_path = os.path.join(exe_path, "backend","lib","GoldbergSteamEmu", 'ColdClientLoader.ini')
    with open(config_file_path, 'w') as configfile:
        config1.write(configfile)
    
    steam_client_loader_path = os.path.join(exe_path, "backend","lib","GoldbergSteamEmu","steamclient_loader.exe")
    steam_client_working_dir = os.path.join(exe_path, "backend","lib","GoldbergSteamEmu")
    subprocess.Popen(steam_client_loader_path, cwd=steam_client_working_dir)
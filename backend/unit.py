import winshell
import jsontoon
import config
import os
from typing import Optional
import winreg
from tkinter import filedialog


def read_registry(
    hive: int,
    reg_path: str,
    key_name: str,
    default: Optional[str] = None
) -> Optional[str]:
    """
    从 Windows 注册表读取指定键的值（支持环境变量展开）
    
    :param hive: 注册表根键，如 winreg.HKEY_CURRENT_USER
    :param reg_path: 注册表路径
    :param key_name: 要读取的键名
    :param default: 读取失败时返回的默认值
    :return: 键值字符串（自动展开环境变量），失败时返回 default
    """
    try:
        with winreg.OpenKey(hive, reg_path) as key:
            value, _ = winreg.QueryValueEx(key, key_name)
            return os.path.expandvars(str(value)) if value else default
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"注册表读取失败 [{hive}\\{reg_path}\\{key_name}]: {e}")
        return default



def add_game_lnk(appid):
    """
    根据给定的 appid 创建游戏快捷方式
    :param appid: 游戏的应用程序 ID
    """
    gameconfig = jsontoon.JSONConfig(config.gameconfig_path)

    df = gameconfig.read(appid)
    icon_path = df["path"]
    app_name = df["name"]
    desktop_raw = read_registry(
        hive=winreg.HKEY_CURRENT_USER,
        reg_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
        key_name="Desktop"
    )

    shortcut = winshell.shortcut()
    shortcut.path = os.getcwd() + "\\startgame.exe"
    shortcut.description = "BY HKXluo"
    shortcut.arguments = f" -appid {appid}"
    shortcut.icon_location = (icon_path, 0)
    shortcut.working_directory = os.getcwd()
    shortcut.write(desktop_raw + f"\\{app_name}.lnk")
    return True

def openFileDialog():
    """
    打开文件对话框，让用户选择游戏文件并添加游戏设置
    :param root: Tkinter 的主窗口对象
    """
    # 打开文件对话框，让用户选择文件
    file_path = filedialog.askopenfilename(title="选择EXE文件",filetypes=[("可执行文件", "*.exe")])
    if file_path == "":
        return

    # 获取文件名、图标和路径
    file_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)

    # 检测文件所在路径是否有 steam_appid.txt 文件
    steam_appid_path = os.path.join(file_dir, "steam_appid.txt")
    if os.path.exists(steam_appid_path):
        # 读取 steam_appid.txt 文件并将其内容存储在表中
        with open(steam_appid_path, "r") as f:
            appid = f.read().strip()
    else:
        # 返回一个包含文件名、文件路径、图标路径和 appid 的空表
        appid = None

    df = {"name": file_name, "path": file_path, "appid": appid}
    print(f"Debug: 已添加游戏，数据: {df}")  # debug 日志输出
    return df
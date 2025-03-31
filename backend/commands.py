from typing import List, Dict
import jsontoon
import config
import unit 
import rungame

userconfig = jsontoon.JSONConfig(config.userconfig_path)
gameconfig = jsontoon.JSONConfig(config.gameconfig_path)

def _convert_dict_to_list(input_dict):
    """
    将字典格式转换为列表格式
    输入: {"123": {"name": "txt"}, ...}
    输出: [{"appid": 123, "name": "txt"}, ...]
    """
    return [{"appid": int(appid), **data} for appid, data in input_dict.items()]

def _convert_list_to_dict(game_data):
    """
    将游戏数据从列表格式转换为字典格式
    输入格式: [{"appid": 123, "name": "游戏"}, ...] 或单个字典
    输出格式: {123: {"name": "游戏"}, ...}
    """
    if isinstance(game_data, dict):
        # 如果是单个字典，提取appid作为key，其余作为value
        appid = game_data.pop('appid')
        return {appid: game_data}
    elif isinstance(game_data, list):
        # 如果是列表，遍历每个字典进行处理
        result = {}
        for item in game_data:
            # 创建副本避免修改原始数据
            appid = item.pop('appid')
            result[appid] = item
        return result

def _get_games():
    """获取游戏列表"""
    games = gameconfig.read()
    return _convert_dict_to_list(games)

class GameManager:
    def test():
        return "后端链接成功"

    def __init__(self):
        self.games = []  # 存储游戏数据的列表

    def get_games(self) -> List[Dict]:
        """获取游戏列表"""
        return _get_games()

    def add_game(self, game: Dict) -> List[Dict]:
        """添加游戏"""
        print("--添加游戏--")
        games = gameconfig.read()
        gameint2 = _convert_list_to_dict(game)
        for i,v in gameint2.items(): games[i] = v
        gameconfig.write(games)

        return _get_games()

    def delete_game(self, appid: str) -> List[Dict]:
        """删除游戏"""
        print("--删除游戏--")
        gameconfig.delete(str(appid))

        return _get_games()

    def update_game(self, game: Dict) -> List[Dict]:
        """更新游戏信息"""
        print("--更新游戏--")
        appid = game.pop("appid")
        gameconfig.write(game,str(appid))
        return _get_games()


    def create_desktop_shortcut(self, appid: str) -> str:
        """创建桌面快捷方式"""
        print("--创建桌面快捷方式--")
        if unit.add_game_lnk(str(appid)):
            return "桌面快捷方式创建成功"
        
        return "游戏未找到"

    def launch_game(self, appid: str) -> str:
        """启动游戏"""
        print("--启动游戏--")
        rungame.startGame(str(appid))
        return True

    def import_steam_games(self) -> List[Dict]:
        """从Steam导入游戏"""
        # 这里实现从Steam导入游戏的逻辑
        steam_games = []  # 从Steam获取的游戏列表
        return steam_games
    


    def getUserSettup(self) -> List[Dict]:
        """获取用户设置"""
        print("--获取用户设置--")
        user_name = jsontoon.read_txt(config.GoldbergUser_path+"account_name.txt")
        port = jsontoon.read_txt(config.GoldbergUser_path+"listen_port.txt")
        steamid = jsontoon.read_txt(config.GoldbergUser_path+"user_steam_id.txt")
        language = jsontoon.read_txt(config.GoldbergUser_path+"language.txt")

        list1 = {"account_name": user_name, "listen_port": port, "steam_id": steamid, "language": language}
        return list1
    
    def setUserSettup(self, user_settup: Dict) -> List[Dict]:
        """设置用户设置"""
        print("--设置用户设置--")
        print(user_settup)
        jsontoon.write_txt(config.GoldbergUser_path+"account_name.txt", user_settup["account_name"])
        jsontoon.write_txt(config.GoldbergUser_path+"listen_port.txt", str(user_settup["listen_port"]))
        jsontoon.write_txt(config.GoldbergUser_path+"user_steam_id.txt", user_settup["steam_id"])
        jsontoon.write_txt(config.GoldbergUser_path+"language.txt", user_settup["language"])
        return True
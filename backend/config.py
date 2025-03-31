import os
import json
from pathlib import Path
local_appdata_path = os.environ.get('LOCALAPPDATA')  # Local 目录

appname = "pysteam-crack"
userconfig_path =local_appdata_path + f"\\{appname}\\userconfig.json"
gameconfig_path = local_appdata_path + f"\\{appname}\\gameconfig.json"





def _create_empty_json(path: Path):
    """内部函数 创建空JSON文件"""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({}, f)  # 写入空字典
        print(f"已创建空JSON文件: {path}")

# 转换路径并确保文件存在
_create_empty_json(Path(gameconfig_path))
_create_empty_json(Path(userconfig_path))
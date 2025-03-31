import json
import os

class JSONConfig:
    def __init__(self, json_path):
        self.json_path = json_path
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"错误: 文件 {self.json_path} 未找到。")
            self.data = {}
        except json.JSONDecodeError:
            print(f"错误: 文件 {self.json_path} 不是有效的 JSON 文件。")
            self.data = {}

    def read(self, *keys):
        current = self.data
        for key in keys:
            if key in current:
                current = current[key]
            else:
                return None
        return current

    def write(self, value, *keys):
        current = self.data
        for i, key in enumerate(keys):
            if i == len(keys) - 1:
                current[key] = value
            else:
                if key not in current:
                    current[key] = {}
                current = current[key]
        try:
            with open(self.json_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"错误: 写入文件 {self.json_path} 时出错: {e}")

    def delete(self, *keys):
        current = self.data
        for i, key in enumerate(keys):
            if i == len(keys) - 1:
                if key in current:
                    del current[key]
                    try:
                        with open(self.json_path, 'w', encoding='utf-8') as file:
                            json.dump(self.data, file, indent=4, ensure_ascii=False)
                        return True
                    except Exception as e:
                        print(f"错误: 写入文件 {self.json_path} 时出错: {e}")
                        return False
                else:
                    print(f"错误: 键 {key} 不存在。")
                    return False
            else:
                if key in current:
                    current = current[key]
                else:
                    print(f"错误: 键 {key} 不存在。")
                    return False





def read_txt(file_path: str) -> str | bool:
    """
    读取txt文件
    :param file_path: 文件路径
    :return: 文件内容/""
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except (FileNotFoundError, PermissionError, UnicodeDecodeError):
        return ""
    
def write_txt(file_path: str, content: str, mode: str = 'w') -> bool:
    """
    写入txt文件（自动创建目录和文件）
    :param file_path: 文件路径
    :param content: 要写入的内容
    :param mode: 'w'-覆盖 / 'a'-追加
    :return: 是否成功
    """
    try:
        # 自动创建目录（如果不存在）
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception:
        return False
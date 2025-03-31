import json


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

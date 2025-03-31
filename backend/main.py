import webview
import os
import sys
import time
import commands
import config

def is_dev_mode():
    """检查是否处于开发模式"""
    return True

# 暴露给前端调用的 Python 函数
def get_server_time():
    return f'Python 服务器时间: {time.strftime("%Y-%m-%d %H:%M:%S")}'


manager = commands.GameManager()
def start_app():
    if is_dev_mode():
        # 开发模式：连接 Vite 服务器
        url = 'http://localhost:5173'
    else:
        # 生产模式：使用构建后的文件
        assets_path = os.path.join(os.path.dirname(__file__), '../dist')
        url = f'file://{os.path.join(assets_path, "index.html")}'
    
    window = webview.create_window(
        config.appname,
        url=url,
        width=800,
        height=600
    )

    window.expose(manager.update_game,
                  manager.create_desktop_shortcut,
                  manager.delete_game,
                  manager.get_games,
                  manager.add_game,
                  manager.getUserSettup,
                  manager.setUserSettup,
                  manager.test
                  )
    
    webview.start()

if __name__ == '__main__':
    start_app()
import webview
import os
import sys
import time
import commands
import config

def is_dev_mode():
    """检查是否处于开发模式"""
    return True

manager = commands.GameManager()



# 暴露给前端调用的 Python 函数
def openWebview(url,name):
    with open("frontend\\src\\steam.html", 'r', encoding='utf-8') as file:
        js_code =  file.read()

    def inject_button():
        window2.evaluate_js(js_code)

    window2 = webview.create_window(
        name,
        url=url,
        width=1000,
        height=700
    )
    window2.expose(manager.SteamOutUrl)
    
    window2.events.loaded += inject_button



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
        width=1000,
        height=700
    )

    window.expose(manager.update_game,
                  manager.create_desktop_shortcut,
                  manager.delete_game,
                  manager.get_games,
                  manager.add_game,
                  manager.getUserSettup,
                  manager.setUserSettup,
                  manager.launch_game,
                  manager.test,
                  openWebview
                  )
    
    webview.start()

if __name__ == '__main__':
    start_app()
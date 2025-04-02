import subprocess
import config


def run_steamcmd(app_id, workshop_id,title,show_notification):

    print(f"开始下载：{app_id} - {workshop_id}")
    show_notification(f'⚠️开始下载 创意工坊物品: {title} 注意：关闭窗口会中断下载', "#FF9800")

    cmd = [config.steamcmd_path+"steamcmd.exe","+login", "anonymous","+force_install_dir ",config.Goldberg_path,"+workshop_download_item", str(app_id), str(workshop_id),"+quit"]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1,encoding="utf-8")

    success = False
    error = False

    while True:
        # 读取一行 stdout
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())  # 实时打印

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
        show_notification(f'❌ 创意工坊物品: {title} 下载失败：{error_message}', "#F44336")
        return False
    elif success:
        print("✅ 下载成功！")
        show_notification(f"✅ 创意工坊物品: {title} 下载成功！", "#4CAF50")
        

        return True


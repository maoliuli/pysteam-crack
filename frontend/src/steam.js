// 1. 拦截所有<a>标签的点击
    document.addEventListener('click', function(e) {
        let target = e.target;
        while (target && target.tagName !== 'A') {
            target = target.parentElement;
            if (!target) return;
        }
        if (target && target.href && !target.hasAttribute('data-no-intercept')) {
            e.preventDefault();
            window.location.href = target.href;
        }
    });
    
    // 2. 拦截window.open
    const originalOpen = window.open;
    window.open = function(url, name, specs) {
        window.location.href = url;
        return null;
    };

    let workshopId = '', appId = '';

    // 3. 创建顶部返回按钮
    const backButton = document.createElement('button');
    backButton.id = 'back-btn';
    backButton.textContent = '← 返回';
    backButton.style.cssText = `
        position: fixed;
        top: 10px;
        left: 10px;
        padding: 5px 10px;
        background: rgba(0, 0, 0, 0.7);
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        z-index: 10001;
        font-size: 14px;
    `;

    // 添加点击事件 - 返回上一页
    backButton.addEventListener('click', function() {
        window.history.back();
    });

    // 添加到页面
    document.body.appendChild(backButton);




    // 6. 增强版信息提取与替换
    async function replaceAndShowSubscription() {
        const targetDiv = document.querySelector('.game_area_purchase_game');
        if (!targetDiv) {
            window.showNotification('未找到 .game_area_purchase_game 元素');
            return;
        }
        // 方法 1：精准提取 SubscribeItem 参数

        const subscribeBtn = document.getElementById('SubscribeItemBtn'); // 直接通过ID获取
        
        if (subscribeBtn) {
            const onclickText = subscribeBtn.getAttribute('onclick');
            
            // 关键修复：正确的正则表达式

            const matches = onclickText.split("'");
            //const matches = onclickText.match("SubscribeItem\s*$\s*'(\d+)'\s*,\s*'(\d+)'\s*$;");

            if (matches) {
                workshopId = matches[1]; // 第一个参数 (3405454008)
                appId = matches[3];      // 第二个参数 (457140)
                //window.showNotification(`提取成功: ${workshopId}, ${appId}`, '#4CAF50');
            } else {
                //window.showNotification('提取失败: 参数格式不匹配', '#F44336');
                window.showNotification(onclickText);
            }
        } else {
            window.showNotification('未找到订阅按钮', '#F44336');
        }
    
        // 改进版标题提取
        let title = '未知标题';
        const titleElement = document.querySelector('.workshopItemTitle') ||  // 方案 1
                            document.querySelector('h1') ||                    // 方案 2
                            document.querySelector('.apphub_AppName');        // 方案 3
        if (titleElement) {
            title = titleElement.textContent
                .replace('订阅以下载', '')
                .replace('Subscribe to download', '')
                .trim();
        }
    
        // --- 构建新内容 ---
        targetDiv.innerHTML = `
            <div id="subscription-info" style="
                padding: 15px;
                margin-bottom: 20px;
                background: #1a1a1a;
                border-radius: 4px;
                color: white;
                border-left: 4px solid #FF5722;
                width: 60%;
            ">
                <h3 style="margin-top: 0; color: #FF5722;">提取的订阅信息</h3>
                <p><strong>模组名称:</strong> ${title}</p>
                <p><strong>AppID:</strong> ${appId || '未提取到'}</p>
                <p><strong>WorkshopID:</strong> ${workshopId || (window.location.href.includes('filedetails') ? '见URL' : '未提取到')}</p>
            </div>
    
            <div style="display: flex; flex-direction: column; align-items: flex-end; padding: 15px; margin-bottom: 20px; background: #1a1a1a; border-radius: 4px; color: white; width: 40%;">
                <h2 id="installation-info" style="white-space: pre-line; text-align: left; margin-right: auto;" >🎮 自定义购买区域</h2>
                
                <div style="display: flex; gap: 10px; margin-top: auto; ">
                    <!-- 删除按钮 - 改为红色，默认隐藏 -->
                    <button id="custom1-btn" style="display: none;padding: 8px 16px; background: #f44336;  /* 红色 */color: white; border: none; border-radius: 4px; cursor: pointer;">
                        删除
                    </button>
                    <!-- 更新按钮 -->
                    <button id="custom-btn" style="padding: 8px 16px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
                        更新
                    </button>
                
                </div>
            </div>
        `;
        
        try {
            const infoText = await window.pywebview.api.GetWorkshopVersion(appId, workshopId);
            if (infoText != "❌未安装:") {
                document.getElementById('custom1-btn').style.display = 'block';
            }
            document.getElementById('installation-info').textContent = infoText;
        } catch (error) {
            document.getElementById('installation-info').textContent = "获取失败: " + error.message;
        }


    
        // --- 按钮事件 ---
        document.getElementById('custom-btn').addEventListener('click', () => {
            if (workshopId && appId) {
                window.pywebview.api.SteamOutUrl(appId,workshopId,title);
            } else {
                window.showNotification('错误: 缺少必要参数', '#F44336');
            }
        });
        document.getElementById('custom1-btn').addEventListener('click', () => {
            if (workshopId && appId) {
                window.pywebview.api.delworkshopId(appId,workshopId,title);
            } else {
                window.showNotification('错误: 缺少必要参数', '#F44336');
            }
        });
        
    }


    

    
    // 延迟执行 + 重试机制
    function init() {
        if (!document.querySelector('.game_area_purchase_game')) {
            setTimeout(init, 500); // 每隔500ms重试直到元素加载
            return;
        }



        replaceAndShowSubscription();
    }


    

    
    // 启动
    init();



    // 3. 创建通知系统（修改版）
    const notificationContainer = document.createElement('div');
    notificationContainer.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        z-index: 10000;
    `;
    document.body.appendChild(notificationContainer);

    // 增强版通知函数
    window.showNotification = function(message, bgColor = 'rgba(0, 0, 0, 0.8)') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            padding: 12px 20px;
            background: ${bgColor};
            color: white;
            border-radius: 4px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            animation: slideIn 0.3s ease-out;
            transition: opacity 0.3s;
            white-space: pre-wrap;
        `;
        
        notification.textContent = message;
        notificationContainer.appendChild(notification);
        
        // 检查消息是否包含特定标识（如当前workshop_id）
        if (message.includes(workshopId) || 
            message.includes('需要刷新')) {
            setTimeout(() => {
                window.location.reload(); // 刷新页面
            }, 15); // 1.5秒后刷新，让用户有时间看到通知
        } else {
            // 普通通知3秒后消失
            setTimeout(() => {
                notification.style.opacity = '0';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }
    };
    
    // 4. 添加动画样式
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);


<script setup lang="ts">
import { ref, onMounted, provide } from "vue";
import userSettings from "./components/user.vue";

// 定义游戏数据接口
interface Game {
  appid: string;
  name: string;
  path: string;
  arguments: string;
  disable_overlay: boolean;
  offline_mode: boolean;
}

const games = ref<Game[]>([]);
const selectedGame = ref<Game | null>(null);
const gameToAdd = ref<Game>({
  appid: "",
  name: "",
  path: "",
  arguments: "",
  disable_overlay: false,
  offline_mode: false

});
const test1 = ref("");
const df = {}
const theme = ref(localStorage.getItem('theme') || 'light'); // 从本地存储读取主题
const message = ref("");
const activeTab = ref("steam"); // 默认显示Steam导入标签页
const showAddGameModal = ref(false); // 添加控制弹窗显示的状态
const isEditing = ref(false); // 是否处于编辑模式
const showSettingsModal = ref(false); // 添加设置弹窗控制
const activeView = ref('games'); // 控制当前显示的视图
function switchView(view: string) { // 切换视图的方法
  activeView.value = view;
}

// 获取游戏列表
async function getGames() {
  try {
    // Python 函数: get_games() -> List[Dict]
    // 返回值: 包含所有游戏信息的数组，每个游戏是字典格式
    games.value = await window.pywebview.api.get_games();
  } catch (error) {
    showMessage(`获取游戏列表失败: ${error}`, "error");
  }
}

// 添加游戏
async function addGame(game: Game) {
  if (!game.appid || !game.name || !game.path) {
    showMessage("请填写完整信息", "warning");
    return;
  }

  const existingGame = games.value.find(g => g.appid === game.appid);
  if (existingGame) {
    showMessage("游戏已存在", "success");
    return;
  }
  
  try {
    // Python 函数: add_game(game: Dict) -> List[Dict]
    // 参数: game - 包含游戏信息的字典 {appid, name, path, icon_path}
    // 返回值: 更新后的游戏列表
    games.value = await window.pywebview.api.add_game(game);
    
    gameToAdd.value = { appid: "", name: "", path: "", icon_path: "" };
    showMessage("游戏添加成功", "success");
  } catch (error) {
    showMessage(`添加游戏失败: ${error}`, "error");
  }
}

// 删除游戏
async function deleteGame(appid: string) {
  try {
    // Python 函数: delete_game(appid: str) -> List[Dict]
    // 参数: appid - 要删除的游戏ID
    // 返回值: 更新后的游戏列表
    games.value = await window.pywebview.api.delete_game(appid);
    
    if (selectedGame.value && selectedGame.value.appid === appid) {
      selectedGame.value = null;
    }
    showMessage("游戏删除成功", "success");
  } catch (error) {
    showMessage(`删除游戏失败: ${error}`, "error");
  }
}

// 更新游戏信息
async function updateGame(game: Game) {
  try {
    // Python 函数: update_game(game: Dict) -> List[Dict]
    // 参数: game - 包含更新后游戏信息的字典
    // 返回值: 更新后的游戏列表
    games.value = await window.pywebview.api.update_game(game);
    
    showMessage("游戏更新成功", "success");
    isEditing.value = false;
    gameToAdd.value = { appid: "", name: "", path: "",  arguments: "", disable_overlay: false, offline_mode: false};
  } catch (error) {
    showMessage(`更新游戏失败: ${error}`, "error");
  }
}

// 创建桌面快捷方式
async function createDesktopShortcut(appid: string) {
  try {
    // Python 函数: create_desktop_shortcut(appid: str) -> str
    // 参数: appid - 要创建快捷方式的游戏ID
    // 返回值: 操作结果消息字符串
    const result = await window.pywebview.api.create_desktop_shortcut(appid);
    showMessage(result, "success");
  } catch (error) {
    showMessage(`创建桌面快捷方式失败: ${error}`, "error");
  }
}

// 启动游戏
async function launchGame(appid: string) {
  try {
    // Python 函数: launch_game(appid: str) -> str
    // 参数: appid - 要启动的游戏ID
    // 返回值: 操作结果消息字符串
    const result = await window.pywebview.api.launch_game(appid);
    showMessage(result, "success");
  } catch (error) {
    showMessage(`启动游戏失败: ${error}`, "error");
  }
}

async function SteamOpen(appid) {
  try {
    // Python 函数: launch_game(appid: str) -> str
    // 参数: appid - 要启动的游戏ID
    // 返回值: 操作结果消息字符串
    const result = await window.pywebview.api.openWebview(`https://steamcommunity.com/app/${appid}/workshop/`,"Steam创意工坊");
    showMessage(result, "success");
  } catch (error) {
    showMessage(`启动失败: ${error}`, "error");
  }
}

// 处理从Steam导入的游戏
async function handleSteamGames(steamGames: Game[]) {
  for (const game of steamGames) {
    try {
      // Python 函数: import_steam_games() -> List[Dict]
      // 返回值: 从Steam导入的游戏列表
      const importedGames = await window.pywebview.api.import_steam_games();
      await addGame(game);
    } catch (error) {
      showMessage(`添加游戏 ${game.name} 失败: ${error}`, "error");
    }
  }
}

async function openFileDialog() {
  try {
    const df = await window.pywebview.api.openFileDialog();
    gameToAdd.value.path = df["path"];
    gameToAdd.value.name = df["name"];
    gameToAdd.value.appid = df["appid"]
  } catch (error) {
    showMessage(`错误： ${error}`, "error");
  }
}

async function openFolderDialog() {
  try {
    const df = await window.pywebview.api.openFolderDialog();
    gameToAdd.value.path = df["path"];
  } catch (error) {
    showMessage(`错误：`, "error");
  }
}






function showMessage(text: string, type: 'success' | 'error' | 'warning' | 'info' = 'info') {
  message.value = text;
  // 设置一个类，用于样式
  const alertElement = document.getElementById('alert-message');
  if (alertElement) {
    alertElement.className = `alert ${type === 'success' 
      ? 'alert-success' 
      : type === 'error' 
        ? 'alert-error' 
        : type === 'warning' 
          ? 'alert-warning' 
          : 'alert-info'}`;
    alertElement.style.display = 'flex';
    
    // 3秒后自动隐藏
    setTimeout(() => {
      if (message.value === text) { // 确保不会清除新消息
        alertElement.style.display = 'none';
        message.value = "";
      }
    }, 3000);
  }
}
provide('showMessage', showMessage);

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', theme.value);
  localStorage.setItem('theme', theme.value); // 保存主题到本地存储
}

// 处理图片加载错误
function handleImageError(event: Event,name: string) {
  const img = event.target as HTMLImageElement;
  if (!img || !img.parentElement) return;
  img.src = './1.png';
  // 确保父容器具备定位上下文
  img.parentElement.style.position = 'relative';
  // 创建或复用文字元素
  let textOverlay = img.parentElement.querySelector('.img-error-text') as HTMLElement;
  if (!textOverlay) {
    textOverlay = document.createElement('div');
    img.parentElement.appendChild(textOverlay);
    // 基础样式
    Object.assign(textOverlay.style, {
      position: 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      pointerEvents: 'none',
      display: 'none' // 默认隐藏
    });
  }
  // 显示文字
  textOverlay.textContent = name;
  textOverlay.style.display = 'block';
  void textOverlay.offsetHeight; 
}

// 开始编辑游戏
function startEditGame(game: Game) {
  gameToAdd.value = { ...game };
  isEditing.value = true;
  showAddGameModal.value = true;
}

// 开始添加游戏
function startAddGame() {
  gameToAdd.value = { appid: "", name: "", path: "",  arguments: "", disable_overlay: false, offline_mode: false};
  isEditing.value = false;
  activeTab.value = 'steam';
  showAddGameModal.value = true;
}

// 处理游戏表单提交
async function handleGameSubmit(game: Game) {
  if (isEditing.value) {
    await updateGame(game);
  } else {
    await addGame(game);
  }
  showAddGameModal.value = false;
}

onMounted(() => {
  document.documentElement.setAttribute('data-theme', theme.value);
  setTimeout(() => {
    getGames();
  }, 300); // 1000ms = 1秒
});
</script>

<template>
  <div class="flex min-h-screen bg-base-100 transition-all duration-300">
    <!-- 导航栏 -->
    <ul class="menu bg-base-200 rounded-box fixed left-0 top-0 h-screen w-16 z-50 flex flex-col">
      <li :class="{ 'bordered bg-base-300': activeView === 'games' }">
        <a class="tooltip tooltip-right" @click="switchView('games')" data-tip="主页">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 p-1" width="1em" height="1em" viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-width="4"><path stroke-linecap="round" stroke-linejoin="round" d="M9 18v24h30V18L24 6z"/><path stroke-linejoin="round" d="M19 29v13h10V29z"/><path stroke-linecap="round" d="M9 42h30"/></g></svg>
        </a>
      </li>
      <li :class="{ 'bordered bg-base-300': activeView === 'account' }">
        <a class="tooltip tooltip-right" @click="switchView('account')" data-tip="账号设置">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 p-1" width="1em" height="1em" viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"><circle cx="24" cy="12" r="8"/><path d="M42 44c0-9.941-8.059-18-18-18S6 34.059 6 44"/></g></svg>
        </a>
      </li>
      <li :class="{ 'bordered bg-base-300': activeView === 'browser' }">
        <a class="tooltip tooltip-right" @click="switchView('browser')" data-tip="内置浏览器">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 p-1" width="1em" height="1em" viewBox="0 0 48 48"><g fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M42 18v22a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V18"/><path stroke="currentColor" stroke-linejoin="round" stroke-width="4" d="M6 8a2 2 0 0 1 2-2h32a2 2 0 0 1 2 2v10H6z"/><path fill="currentColor" fill-rule="evenodd" d="M12 14a2 2 0 1 0 0-4a2 2 0 0 0 0 4m6 0a2 2 0 1 0 0-4a2 2 0 0 0 0 4m6 0a2 2 0 1 0 0-4a2 2 0 0 0 0 4" clip-rule="evenodd"/></g></svg>
        </a>
      </li>
      
      <div class="mt-auto">
        <li class="mb-2" @click="startAddGame">
          <a class="tooltip tooltip-right" data-tip="添加游戏">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 p-1" width="1em" height="1em" viewBox="0 0 48 48"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M16 6H8a2 2 0 0 0-2 2v8m10 26H8a2 2 0 0 1-2-2v-8m26 10h8a2 2 0 0 0 2-2v-8M32 6h8a2 2 0 0 1 2 2v8m-10 8H16m8 8V16"/></svg>
          </a>
        </li>
        <li class="mb-2" @click="toggleTheme">
          <a class="tooltip tooltip-right" data-tip="切换主题">
            <svg v-if="theme === 'light'" class="w-8 h-8 mb-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z"/>
            </svg>
            <svg v-else class="w-8 h-8 mb-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z"/>
            </svg>

          </a>
        </li>
      
        <li :class="{ 'bordered bg-base-300': activeView === 'setup' }">
          <a class="tooltip tooltip-right" @click="switchView('setup')" data-tip="设置">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 p-1" width="1em" height="1em" viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="4"><path d="m24 4l-6 6h-8v8l-6 6l6 6v8h8l6 6l6-6h8v-8l6-6l-6-6v-8h-8z"/><path d="M24 30a6 6 0 1 0 0-12a6 6 0 0 0 0 12Z"/></g></svg>
          </a>
        </li>
      </div>
    </ul>
    
    <!--导航栏结束-->

    <!-- 主内容区：游戏列表 -->
    <div class="main-content" v-if="activeView === 'games'">
    <!--div class="flex-1 container mx-auto p-4 ml-16 overflow-y-auto h-screen"-->



      <div v-if="games.length > 0" class="game-box">
        <div v-for="game in games" :key="game.appid" class="game-box1 card bg-base-100 shadow-xl" >
          
          <figure class="relative">
            <div class="position-relative aspect-ratio-3/2 hover-scale">
              <img
                :src="`https://cdn.cloudflare.steamstatic.com/steam/apps/${game.appid}/library_600x900.jpg`"
                :alt="game.name"
                @dblclick="launchGame(game.appid)"
                @error.once="handleImageError($event, game.name)"
              />
              <!--h2 class="position-absolute top-1 left-1">123</h2-->
            </div>
          </figure>
          <div class="flex">
            <h2 class="text-sm opacity-70  rounded p-1">
              {{ game.appid }}
            </h2>
            <div class="flex justify-end w-full">
              <div class="dropdown  dropdown-end">
                <div tabindex="0" role="button" class="btn m-1 h-5">...</div>
                <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-1 w-34 p-2 shadow-sm">
                  <button class="btn btn-soft btn-accent" @click="launchGame(game.appid)">启动</button>
                  <button class="btn btn-soft btn-accent" @click="SteamOpen(game.appid)">打开创意工坊</button>
                  <button class="btn btn-soft btn-info"  @click="createDesktopShortcut(game.appid)">创建快捷方式</button>
                  <button class="btn btn-soft btn-primary" @click="startEditGame(game)">编辑</button>
                  <button class="btn btn-soft btn-error" @click="deleteGame(game.appid)">删除</button>
                </ul>
              </div>
            </div>
          </div>
        </div>
      
      </div>
      <div v-else class="text-center py-8">
        <p class="text-lg opacity-50">暂无游戏，点击左下角"添加游戏"开始添加</p>
      </div>
    </div>

    <div class="main-content" v-if="activeView === 'browser'">
      <browser />
    </div>

    <div class="main-content" v-if="activeView === 'account'">
      <userSettings />
    </div>

    <!-- 设置区 -->
    <div class="main-content" v-if="activeView === 'setup'">
    </div>

    <!--消息框-->
    <div class="toast toast-top toast-end">
      <div id="alert-message" class="alert alert-info" style="display: none;">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        <span>{{ message }}</span>
      </div>
    </div>




    <!-- 添加游戏弹窗 -->
    <dialog :class="{ 'modal': true, 'modal-open': showAddGameModal }">
      <div class="modal-box w-11/12 max-w-5xl">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold text-lg">{{ isEditing ? '编辑游戏' : '添加游戏' }}</h3>
          <button class="btn btn-sm btn-circle btn-ghost" @click="showAddGameModal = false">✕</button>
        </div>
        
        <div v-if="!isEditing" class="tabs tabs-boxed mb-4">
          <a class="tab" :class="{ 'tab-active': activeTab === 'steam' }" @click="activeTab = 'steam'">从Steam导入</a>
          <a class="tab" :class="{ 'tab-active': activeTab === 'manual' }" @click="activeTab = 'manual'">手动添加</a>
        </div>

        <!-- Steam游戏导入 -->
        <div v-if="!isEditing && activeTab === 'steam'" class="max-h-[70vh] overflow-y-auto">
          <SteamGames 
            :existing-games="games" 
            @add-games="(games) => { handleSteamGames(games); showAddGameModal = false; }" 
          />
        </div>



        <!-- 手动添加/编辑表单 -->
        <div v-if="isEditing || activeTab === 'manual'" class="form-control">
          
          <div class="flex w-full gap-4">
            <fieldset class="fieldset w-xs bg-base-200 border border-base-300 p-4 rounded-box">
              <label class="fieldset-label">游戏ID</label>
              <input v-model="gameToAdd.appid" type="text" class="input" placeholder="输入游戏SteamAppID" :disabled="isEditing" />

              <label class="fieldset-label">游戏名称</label>
              <input v-model="gameToAdd.name" type="text" class="input" placeholder="输入游戏名" />

              <label class="fieldset-label">游戏目录</label>
              <div class="flex w-full" >
                <input v-model="gameToAdd.path" type="text" class="input" placeholder="输入游戏安装目录" />
                <button class="btn btn-neutral join-item" @click="openFileDialog">浏览</button>
              </div>

              <label class="fieldset-label">启动参数</label>
              <label class="input">
                <input v-model="gameToAdd.arguments" type="text" class="grow" placeholder="启动参数" />
                <span class="badge badge-neutral badge-xs">可选</span>
              </label>
              <div class="flex w-full">
                <fieldset class="fieldset p-2 bg-base-100 border border-base-300 rounded-box w-32">
                  <legend class="fieldset-legend">离线启动</legend>
                  <input v-model="gameToAdd.offline_mode" type="checkbox" checked="checked" class="toggle toggle-warning" />
                </fieldset>
                <fieldset class="fieldset p-2 bg-base-100 border border-base-300 rounded-box w-32">
                  <legend class="fieldset-legend">禁用游戏内覆盖</legend>
                  <input v-model="gameToAdd.disable_overlay" type="checkbox" checked="checked" class="toggle toggle-warning" />
                </fieldset>
              </div>
            </fieldset>

            <fieldset class="fieldset w-xs bg-base-200 border border-base-300 p-4 rounded-box">
              <label class="fieldset-label">游戏启动项</label>

            </fieldset>

          </div>
          
          <div class="mt-4 flex justify-between">
            <button @click="showAddGameModal = false" class="btn">取消</button>
            <button @click="handleGameSubmit(gameToAdd)" class="btn btn-primary">
              {{ isEditing ? '保存修改' : '添加游戏' }}
            </button>
          </div>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button @click="showAddGameModal = false">关闭</button>
      </form>
    </dialog>


    <!-- 设置弹窗 -->
    <dialog :class="{ 'modal': true, 'modal-open': showSettingsModal }">
      <div class="modal-box w-11/12 max-w-5xl">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold text-lg">设置</h3>
          <button class="btn btn-sm btn-circle btn-ghost" @click="showSettingsModal = false">✕</button>
        </div>
        <Settings />
      </div>
    </dialog>
  </div>
</template>

<style scoped>
.main-content {
  margin-left: 4rem;
  flex: 1;
  padding: 1rem;
  height: 100vh;
  overflow-y: auto;
  background-color: hsl(var(--b3));
}

.modal-box {
  max-height: 90vh;
}

.btn-ghost {
  background-color: transparent;
  color: inherit;
  border: 1px solid #ced4da;
}


.hover-scale {
  transition: transform 0.3s ease;
}

.hover-scale:hover {
  transform: scale(1.1);
}

.game-box {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 10px
}

.game-box1 {
  aspect-ratio: 3/2;
}

.img-error-text {
  color: white;
  font-size: 1.2rem;
  background: rgba(255, 0, 0, 0.3);
  padding: 8px 16px;
  border-radius: 4px;
  backdrop-filter: blur(2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>

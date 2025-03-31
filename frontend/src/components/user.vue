<template>
    <div class="settings-container">
      <h2>账户设置</h2>
      
      <!-- 基本设置 -->
      <div class="settings-section">
        <div class="form-group">
          <label>账户名称</label>
          <input v-model="settings.account_name" type="text" placeholder="输入账户名称" />
        </div>
        <div class="form-group">
          <label>监听端口</label>
          <input v-model="settings.listen_port" type="number" placeholder="默认端口" />
        </div>
        <div class="form-group">
          <label>Steam ID</label>
          <input v-model="settings.steam_id" type="text" placeholder="输入Steam ID" />
        </div>
        <div class="form-group">
          <label>语言</label>
          <select v-model="settings.language">
            <option value="schinese">简体中文</option>
            <option value="english">English</option>
            <option value="tchinese">繁體中文</option>
            <!-- 其他语言选项 -->
          </select>
        </div>
        <button class="btn btn-soft btn-primary" @click="saveUserSettup">保存设置</button>
      </div>
        
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, inject } from "vue";

interface Settings {
account_name: string
listen_port: number
steam_id: string
language: string
}
const showMessage = inject('showMessage');
const settings = ref<Settings>({
    account_name: '',
    listen_port: 47584,
    steam_id: '',
    language: 'schinese',
})

async function getUserSettup() {
  const result = await window.pywebview.api.getUserSettup();
  settings.value = result;
}

async function saveUserSettup() {
  const result = await window.pywebview.api.setUserSettup(settings.value);
  if (result) {
    showMessage('保存成功');
  } else {
    showMessage('保存失败');
  }
}

onMounted(() => {
  setTimeout(() => {
    getUserSettup()
  }, 300); // 1000ms = 1秒
});
</script>

<style scoped>
.settings-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.settings-section {
  
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="text"],
input[type="number"],
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
}

.dlc-item,
.ip-item,
.language-item,
.depot-item,
.group-item,
.app-path-item,
.stat-item,
.leaderboard-item {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.remove-btn {
  background: #ff4444;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.add-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.save-btn {
  background: #2196F3;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px;
}

button:hover {
  opacity: 0.9;
}
</style> 
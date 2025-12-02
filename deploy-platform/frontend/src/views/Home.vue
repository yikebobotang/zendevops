<template>
  <el-container class="home-container">
    <!-- 顶部导航栏 -->
    <el-header class="home-header">
      <div class="header-left">
        <el-icon class="logo-icon"><Setting /></el-icon>
        <h1>部署平台</h1>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-avatar :size="32" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
            <span class="username">{{ username }}</span>
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item divided command="logout">
                <el-icon><SwitchButton /></el-icon>
                <span>退出登录</span>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    
    <el-container>
      <!-- 侧边栏 -->
      <el-aside class="home-aside" width="200px">
        <el-menu 
          :default-active="activeMenu" 
          class="aside-menu"
          router
          :unique-opened="true"
        >
          <el-menu-item index="/home">
            <el-icon><House /></el-icon>
            <template #title>首页</template>
          </el-menu-item>
          <el-menu-item index="/deploy">
            <el-icon><Upload /></el-icon>
            <template #title>部署配置</template>
          </el-menu-item>
          <el-menu-item index="/logs">
            <el-icon><Document /></el-icon>
            <template #title>部署日志</template>
          </el-menu-item>
          <el-menu-item index="/users">
            <el-icon><User /></el-icon>
            <template #title>用户管理</template>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-main class="home-main">
        <div class="main-header">
          <h2>欢迎使用部署平台</h2>
          <p>高效管理和部署您的中间件服务</p>
        </div>
        
        <div class="card-container">
          <el-card class="stat-card" shadow="hover">
            <div class="card-content">
              <div class="card-icon blue">
                <el-icon><Monitor /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">已部署服务</div>
                <div class="card-value">0</div>
              </div>
            </div>
          </el-card>
          
          <el-card class="stat-card" shadow="hover">
            <div class="card-content">
              <div class="card-icon green">
                <el-icon><CircleCheck /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">成功部署</div>
                <div class="card-value">0</div>
              </div>
            </div>
          </el-card>
          
          <el-card class="stat-card" shadow="hover">
            <div class="card-content">
              <div class="card-icon orange">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">部署失败</div>
                <div class="card-value">0</div>
              </div>
            </div>
          </el-card>
          
          <el-card class="stat-card" shadow="hover">
            <div class="card-content">
              <div class="card-icon purple">
                <el-icon><User /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">系统用户</div>
                <div class="card-value">1</div>
              </div>
            </div>
          </el-card>
        </div>
        
        <div class="quick-actions">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <span>快速操作</span>
              </div>
            </template>
            <div class="action-buttons">
              <el-button type="primary" size="large" @click="$router.push('/deploy')">
                <el-icon><Upload /></el-icon>
                新部署
              </el-button>
              <el-button type="success" size="large" @click="$router.push('/logs')">
                <el-icon><Document /></el-icon>
                查看日志
              </el-button>
              <el-button type="info" size="large" @click="$router.push('/users')">
                <el-icon><User /></el-icon>
                用户管理
              </el-button>
            </div>
          </el-card>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { ref, computed } from 'vue'
import { 
  Setting, 
  ArrowDown, 
  House, 
  Upload, 
  Document, 
  User, 
  Monitor, 
  CircleCheck, 
  Warning, 
  SwitchButton 
} from '@element-plus/icons-vue'

export default {
  name: 'Home',
  components: {
    Setting,
    ArrowDown,
    House,
    Upload,
    Document,
    User,
    Monitor,
    CircleCheck,
    Warning,
    SwitchButton
  },
  setup() {
    const username = ref('admin')
    
    const activeMenu = computed(() => {
      return window.location.pathname
    })
    
    const handleCommand = (command) => {
      if (command === 'logout') {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
    }
    
    return {
      username,
      activeMenu,
      handleCommand
    }
  }
}
</script>

<style scoped>
.home-container {
  height: 100vh;
}

.home-header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 24px;
  color: #667eea;
}

.header-left h1 {
  color: #333;
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.username {
  color: #333;
  font-size: 14px;
  font-weight: 500;
}

.home-aside {
  background-color: #fff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
}

.aside-menu {
  height: 100%;
  border-right: none;
}

.home-main {
  background-color: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}

.main-header {
  margin-bottom: 20px;
}

.main-header h2 {
  color: #333;
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.main-header p {
  color: #666;
  font-size: 1rem;
  margin: 0;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 12px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.card-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

.card-icon.blue {
  background-color: #ecf5ff;
  color: #409eff;
}

.card-icon.green {
  background-color: #f0f9eb;
  color: #67c23a;
}

.card-icon.orange {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.card-icon.purple {
  background-color: #f9f0ff;
  color: #909399;
}

.card-info {
  flex: 1;
}

.card-title {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.card-value {
  color: #333;
  font-size: 24px;
  font-weight: 600;
}

.quick-actions {
  margin-top: 20px;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  padding: 20px 0;
}

:deep(.el-menu-item.is-active) {
  background-color: #ecf5ff !important;
  color: #409eff !important;
}

:deep(.el-menu-item:hover) {
  background-color: #f5f7fa !important;
}
</style>
<template>
  <el-container class="logs-container">
    <!-- 顶部导航栏 -->
    <el-header class="logs-header">
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
      <el-aside class="logs-aside" width="200px">
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
      <el-main class="logs-main">
        <div class="main-header">
          <h2>部署日志</h2>
        </div>
        
        <el-card shadow="hover" class="logs-card">
          <template #header>
            <div class="card-header">
              <span>部署历史</span>
              <el-input
                v-model="searchQuery"
                placeholder="搜索部署ID..."
                clearable
                size="small"
                class="search-input"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>
          </template>
          
          <div v-if="!selectedLog">
            <el-table :data="filteredLogs" stripe style="width: 100%" @row-click="selectLog">
              <el-table-column prop="deploy_id" label="部署ID" min-width="200" />
              <el-table-column prop="log_file" label="日志文件" min-width="150" />
              <el-table-column label="文件大小" min-width="100">
                <template #default="scope">
                  {{ formatSize(scope.row.size) }}
                </template>
              </el-table-column>
              <el-table-column label="创建时间" min-width="180">
                <template #default="scope">
                  {{ formatTime(scope.row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" min-width="120" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="selectLog(scope.row)">
                    <el-icon><Document /></el-icon>
                    查看
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="empty-state" v-if="filteredLogs.length === 0">
              <el-empty description="暂无部署日志" />
            </div>
          </div>
          
          <div v-else>
            <div class="detail-header">
              <h3>部署日志详情</h3>
              <el-button @click="selectedLog = null" size="small">
                <el-icon><Back /></el-icon>
                返回列表
              </el-button>
            </div>
            
            <el-descriptions :column="2" border class="log-meta-info">
              <el-descriptions-item label="部署ID">{{ selectedLog.deploy_id }}</el-descriptions-item>
              <el-descriptions-item label="日志文件">{{ selectedLog.log_file }}</el-descriptions-item>
              <el-descriptions-item label="文件大小">{{ formatSize(selectedLog.size) }}</el-descriptions-item>
              <el-descriptions-item label="创建时间">{{ formatTime(selectedLog.created_at) }}</el-descriptions-item>
            </el-descriptions>
            
            <div class="log-content">
              <el-card shadow="never" class="content-card">
                <template #header>
                  <div class="content-header">
                    <span>日志内容</span>
                  </div>
                </template>
                <pre v-if="logContent">{{ logContent }}</pre>
                <div class="loading" v-else>
                  <el-skeleton :rows="10" animated />
                </div>
              </el-card>
            </div>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { 
  Setting, 
  ArrowDown, 
  House, 
  Upload, 
  Document, 
  User, 
  SwitchButton, 
  Search, 
  Back 
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'Logs',
  components: {
    Setting,
    ArrowDown,
    House,
    Upload,
    Document,
    User,
    SwitchButton,
    Search,
    Back
  },
  setup() {
    const username = ref('admin')
    const logs = ref([])
    const searchQuery = ref('')
    const selectedLog = ref(null)
    const logContent = ref(null)
    
    // 从URL获取部署ID
    const getDeployIdFromUrl = () => {
      const urlParams = new URLSearchParams(window.location.search)
      return urlParams.get('deploy_id')
    }
    
    // 加载日志列表
    const loadLogs = async () => {
      try {
        const response = await axios.get('/api/logs')
        logs.value = response.data
        
        // 如果URL中有部署ID，自动加载该日志
        const deployId = getDeployIdFromUrl()
        if (deployId) {
          const log = logs.value.find(l => l.deploy_id === deployId)
          if (log) {
            selectLog(log)
          }
        }
      } catch (err) {
        console.error('加载日志列表失败:', err)
      }
    }
    
    // 选择日志
    const selectLog = async (log) => {
      selectedLog.value = log
      logContent.value = null
      try {
        const response = await axios.get(`/api/logs?deploy_id=${log.deploy_id}`)
        logContent.value = response.data.content
      } catch (err) {
        console.error('加载日志内容失败:', err)
        logContent.value = '加载日志失败'
      }
    }
    
    // 格式化文件大小
    const formatSize = (size) => {
      if (size < 1024) {
        return `${size} B`
      } else if (size < 1024 * 1024) {
        return `${(size / 1024).toFixed(2)} KB`
      } else {
        return `${(size / (1024 * 1024)).toFixed(2)} MB`
      }
    }
    
    // 格式化时间
    const formatTime = (timestamp) => {
      const date = new Date(timestamp)
      return date.toLocaleString()
    }
    
    // 过滤后的日志列表
    const filteredLogs = computed(() => {
      if (!searchQuery.value) {
        return logs.value
      }
      return logs.value.filter(log => 
        log.deploy_id.includes(searchQuery.value)
      )
    })
    
    // 激活的菜单
    const activeMenu = computed(() => {
      return window.location.pathname
    })
    
    // 退出登录
    const handleCommand = (command) => {
      if (command === 'logout') {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
    }
    
    onMounted(() => {
      loadLogs()
    })
    
    return {
      username,
      logs,
      searchQuery,
      selectedLog,
      logContent,
      filteredLogs,
      activeMenu,
      selectLog,
      formatSize,
      formatTime,
      handleCommand
    }
  }
}
</script>

<style scoped>
.logs-container {
  height: 100vh;
}

.logs-header {
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

.logs-aside {
  background-color: #fff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
}

.aside-menu {
  height: 100%;
  border-right: none;
}

.logs-main {
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
  margin: 0;
}

.logs-card {
  border-radius: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-input {
  width: 250px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.detail-header h3 {
  color: #333;
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0;
}

.log-meta-info {
  margin-bottom: 20px;
}

.log-content {
  margin-top: 20px;
}

.content-card {
  border-radius: 8px;
}

.content-header span {
  color: #333;
  font-size: 1rem;
  font-weight: 500;
}

.log-content pre {
  padding: 20px;
  margin: 0;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9rem;
  line-height: 1.6;
  background-color: #fafafa;
  color: #333;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 500px;
  overflow-y: auto;
  border-radius: 8px;
}

.loading {
  padding: 20px;
}

.empty-state {
  padding: 40px 0;
  text-align: center;
}

:deep(.el-menu-item.is-active) {
  background-color: #ecf5ff !important;
  color: #409eff !important;
}

:deep(.el-menu-item:hover) {
  background-color: #f5f7fa !important;
}

:deep(.el-button--primary) {
  background-color: #667eea;
  border-color: #667eea;
}

:deep(.el-button--primary:hover) {
  background-color: #5a6fd8;
  border-color: #5a6fd8;
}
</style>
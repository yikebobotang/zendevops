<template>
  <el-container class="deploy-container">
    <!-- 顶部导航栏 -->
    <el-header class="deploy-header">
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
      <el-aside class="deploy-aside" width="200px">
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
      <el-main class="deploy-main">
        <div class="main-header">
          <h2>部署配置</h2>
        </div>
        
        <el-card shadow="hover" class="deploy-card">
          <el-form 
            :model="form" 
            :rules="rules" 
            ref="formRef"
            label-width="120px"
            @submit.prevent="handleDeploy"
          >
            <el-form-item prop="serviceType">
              <label>服务类型</label>
              <el-select 
                v-model="form.serviceType" 
                placeholder="请选择服务类型"
                @change="onServiceTypeChange"
                style="width: 100%"
              >
                <el-option value="">请选择服务类型</el-option>
                <el-option 
                  v-for="service in services" 
                  :key="service.name" 
                  :label="service.display_name" 
                  :value="service.name"
                />
              </el-select>
            </el-form-item>
            
            <!-- MySQL配置 -->
            <template v-if="form.serviceType === 'mysql'">
              <el-divider content-position="left">MySQL配置</el-divider>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item prop="config.port">
                    <label>端口</label>
                    <el-input 
                      v-model.number="form.config.port" 
                      placeholder="3306"
                      type="number"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item prop="config.root_password">
                    <label>Root密码</label>
                    <el-input 
                      v-model="form.config.root_password" 
                      placeholder="请输入密码"
                      type="password"
                      show-password
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item prop="config.database">
                <label>初始数据库</label>
                <el-input 
                  v-model="form.config.database" 
                  placeholder="myapp"
                />
              </el-form-item>
            </template>
            
            <!-- Redis配置 -->
            <template v-else-if="form.serviceType === 'redis'">
              <el-divider content-position="left">Redis配置</el-divider>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item prop="config.port">
                    <label>端口</label>
                    <el-input 
                      v-model.number="form.config.port" 
                      placeholder="6379"
                      type="number"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item prop="config.password">
                    <label>密码</label>
                    <el-input 
                      v-model="form.config.password" 
                      placeholder="请输入密码"
                      type="password"
                      show-password
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item prop="config.maxmemory">
                <label>最大内存(MB)</label>
                <el-input 
                  v-model.number="form.config.maxmemory" 
                  placeholder="1024"
                  type="number"
                />
              </el-form-item>
            </template>
            
            <!-- ZooKeeper配置 -->
            <template v-else-if="form.serviceType === 'zookeeper'">
              <el-divider content-position="left">ZooKeeper配置</el-divider>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item prop="config.client_port">
                    <label>客户端端口</label>
                    <el-input 
                      v-model.number="form.config.client_port" 
                      placeholder="2181"
                      type="number"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item prop="config.server_port">
                    <label>服务器端口</label>
                    <el-input 
                      v-model.number="form.config.server_port" 
                      placeholder="2888"
                      type="number"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item prop="config.leader_port">
                <label>选举端口</label>
                <el-input 
                  v-model.number="form.config.leader_port" 
                  placeholder="3888"
                  type="number"
                />
              </el-form-item>
            </template>
            
            <el-form-item>
              <div class="form-actions">
                <el-button type="primary" native-type="submit" :loading="isDeploying" size="large">
                  {{ isDeploying ? '部署中...' : '开始部署' }}
                </el-button>
                <el-button @click="$router.go(-1)" size="large">
                  返回
                </el-button>
              </div>
            </el-form-item>
          </el-form>
        </el-card>
        
        <!-- 部署结果 -->
        <el-card shadow="hover" class="result-card" v-if="deployResult">
          <template #header>
            <div class="result-header">
              <h3>部署结果</h3>
            </div>
          </template>
          <div class="result-content">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="状态">
                <el-tag :type="deployResult.status === 'success' ? 'success' : 'error'">
                  {{ deployResult.status }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="消息">{{ deployResult.message }}</el-descriptions-item>
              <el-descriptions-item label="部署ID" v-if="deployResult.deploy_id">{{ deployResult.deploy_id }}</el-descriptions-item>
            </el-descriptions>
            <div class="result-actions" v-if="deployResult.deploy_id">
              <el-button type="primary" @click="viewLogs">
                <el-icon><Document /></el-icon>
                查看部署日志
              </el-button>
            </div>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { 
  Setting, 
  ArrowDown, 
  House, 
  Upload, 
  Document, 
  User, 
  SwitchButton 
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'Deploy',
  components: {
    Setting,
    ArrowDown,
    House,
    Upload,
    Document,
    User,
    SwitchButton
  },
  setup() {
    const username = ref('admin')
    const services = ref([])
    const formRef = ref(null)
    const isDeploying = ref(false)
    const deployResult = ref(null)
    
    const form = reactive({
      serviceType: '',
      config: {}
    })
    
    const rules = {
      serviceType: [
        { required: true, message: '请选择服务类型', trigger: 'change' }
      ],
      'config.port': [
        { required: true, message: '请输入端口', trigger: 'blur' },
        { type: 'number', message: '请输入有效的端口号', trigger: 'blur' }
      ],
      'config.root_password': [
        { required: true, message: '请输入Root密码', trigger: 'blur' }
      ],
      'config.password': [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ],
      'config.client_port': [
        { required: true, message: '请输入客户端端口', trigger: 'blur' },
        { type: 'number', message: '请输入有效的端口号', trigger: 'blur' }
      ],
      'config.server_port': [
        { required: true, message: '请输入服务器端口', trigger: 'blur' },
        { type: 'number', message: '请输入有效的端口号', trigger: 'blur' }
      ],
      'config.leader_port': [
        { required: true, message: '请输入选举端口', trigger: 'blur' },
        { type: 'number', message: '请输入有效的端口号', trigger: 'blur' }
      ]
    }
    
    const activeMenu = ref('/deploy')
    
    const loadServices = async () => {
      try {
        const response = await axios.get('/api/services')
        services.value = response.data
      } catch (err) {
        console.error('加载服务列表失败:', err)
      }
    }
    
    const onServiceTypeChange = () => {
      // 重置配置为默认值
      form.config = {}
      if (form.serviceType === 'mysql') {
        form.config = {
          port: 3306,
          database: 'myapp'
        }
      } else if (form.serviceType === 'redis') {
        form.config = {
          port: 6379,
          maxmemory: 1024
        }
      } else if (form.serviceType === 'zookeeper') {
        form.config = {
          client_port: 2181,
          server_port: 2888,
          leader_port: 3888
        }
      }
    }
    
    const handleDeploy = async () => {
      try {
        await formRef.value.validate()
        isDeploying.value = true
        deployResult.value = null
        
        const response = await axios.post('/api/deploy', {
          service_type: form.serviceType,
          config: form.config
        })
        deployResult.value = response.data
      } catch (err) {
        deployResult.value = {
          status: 'error',
          message: err.response?.data?.message || '部署失败'
        }
      } finally {
        isDeploying.value = false
      }
    }
    
    const viewLogs = () => {
      if (deployResult.value.deploy_id) {
        // 跳转到日志页面并传递部署ID
        window.location.href = `/logs?deploy_id=${deployResult.value.deploy_id}`
      }
    }
    
    const handleCommand = (command) => {
      if (command === 'logout') {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
    }
    
    onMounted(() => {
      loadServices()
    })
    
    return {
      username,
      services,
      formRef,
      form,
      rules,
      isDeploying,
      deployResult,
      activeMenu,
      onServiceTypeChange,
      handleDeploy,
      viewLogs,
      handleCommand
    }
  }
}
</script>

<style scoped>
.deploy-container {
  height: 100vh;
}

.deploy-header {
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

.deploy-aside {
  background-color: #fff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
}

.aside-menu {
  height: 100%;
  border-right: none;
}

.deploy-main {
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

.deploy-card {
  border-radius: 12px;
  margin-bottom: 20px;
}

.form-actions {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
  margin-top: 20px;
}

.result-card {
  border-radius: 12px;
  margin-top: 20px;
}

.result-header h3 {
  color: #333;
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0;
}

.result-content {
  padding: 10px 0;
}

.result-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
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
<template>
  <el-container class="users-container">
    <!-- 顶部导航栏 -->
    <el-header class="users-header">
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
      <el-aside class="users-aside" width="200px">
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
      <el-main class="users-main">
        <div class="main-header">
          <h2>用户管理</h2>
          <el-button type="primary" @click="openCreateDialog">
            <el-icon><Plus /></el-icon>
            新增用户
          </el-button>
        </div>
        
        <el-card shadow="hover" class="users-card">
          <template #header>
            <div class="card-header">
              <span>用户列表</span>
              <el-input
                v-model="searchQuery"
                placeholder="搜索用户名"
                clearable
                size="small"
                class="search-input"
                @input="handleSearch"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>
          </template>
          
          <el-table :data="filteredUsers" stripe style="width: 100%">
            <el-table-column prop="username" label="用户名" min-width="150" />
            <el-table-column prop="role" label="角色" min-width="100">
              <template #default="scope">
                <el-tag :type="scope.row.role === 'admin' ? 'warning' : 'success'">
                  {{ scope.row.role === 'admin' ? '管理员' : '普通用户' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="email" label="邮箱" min-width="200" />
            <el-table-column prop="created_at" label="创建时间" min-width="180" />
            <el-table-column label="操作" min-width="150" fixed="right">
              <template #default="scope">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="openEditDialog(scope.row)"
                  :disabled="scope.row.username === 'admin'"
                >
                  <el-icon><Edit /></el-icon>
                  编辑
                </el-button>
                <el-button 
                  type="danger" 
                  size="small" 
                  @click="openDeleteDialog(scope.row)"
                  :disabled="scope.row.username === 'admin'"
                >
                  <el-icon><Delete /></el-icon>
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
        <!-- 新增用户对话框 -->
        <el-dialog
          v-model="createDialogVisible"
          title="新增用户"
          width="500px"
          @close="resetCreateForm"
        >
          <el-form :model="createForm" :rules="rules" ref="createFormRef" label-width="100px">
            <el-form-item prop="username">
              <el-input v-model="createForm.username" placeholder="请输入用户名" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="createForm.password" type="password" placeholder="请输入密码" show-password />
            </el-form-item>
            <el-form-item prop="email">
              <el-input v-model="createForm.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item prop="role">
              <el-select v-model="createForm.role" placeholder="请选择角色">
                <el-option label="管理员" value="admin" />
                <el-option label="普通用户" value="user" />
              </el-select>
            </el-form-item>
          </el-form>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="createDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="handleCreate">确定</el-button>
            </span>
          </template>
        </el-dialog>
        
        <!-- 编辑用户对话框 -->
        <el-dialog
          v-model="editDialogVisible"
          title="编辑用户"
          width="500px"
          @close="resetEditForm"
        >
          <el-form :model="editForm" :rules="rules" ref="editFormRef" label-width="100px">
            <el-form-item prop="username">
              <el-input v-model="editForm.username" placeholder="请输入用户名" disabled />
            </el-form-item>
            <el-form-item prop="password" label="新密码">
              <el-input v-model="editForm.password" type="password" placeholder="留空则不修改" show-password />
            </el-form-item>
            <el-form-item prop="email">
              <el-input v-model="editForm.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item prop="role">
              <el-select v-model="editForm.role" placeholder="请选择角色">
                <el-option label="管理员" value="admin" />
                <el-option label="普通用户" value="user" />
              </el-select>
            </el-form-item>
          </el-form>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="editDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="handleEdit">确定</el-button>
            </span>
          </template>
        </el-dialog>
        
        <!-- 删除确认对话框 -->
        <el-dialog
          v-model="deleteDialogVisible"
          title="确认删除"
          width="400px"
        >
          <div class="delete-content">
            <el-icon class="warning-icon"><Warning /></el-icon>
            <p>确定要删除用户 <span class="username-text">{{ deleteUser.username }}</span> 吗？</p>
            <p class="delete-hint">此操作不可恢复，请谨慎操作！</p>
          </div>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="deleteDialogVisible = false">取消</el-button>
              <el-button type="danger" @click="handleDelete">确定删除</el-button>
            </span>
          </template>
        </el-dialog>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'
import { 
  Setting, 
  ArrowDown, 
  House, 
  Upload, 
  Document, 
  User, 
  SwitchButton, 
  Plus, 
  Search, 
  Edit, 
  Delete, 
  Warning 
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'Users',
  components: {
    Setting,
    ArrowDown,
    House,
    Upload,
    Document,
    User,
    SwitchButton,
    Plus,
    Search,
    Edit,
    Delete,
    Warning
  },
  setup() {
    const username = ref('admin')
    const users = ref([])
    const searchQuery = ref('')
    
    // 对话框状态
    const createDialogVisible = ref(false)
    const editDialogVisible = ref(false)
    const deleteDialogVisible = ref(false)
    
    // 表单引用
    const createFormRef = ref(null)
    const editFormRef = ref(null)
    
    // 当前操作的用户
    const deleteUser = ref({})
    
    // 表单数据
    const createForm = reactive({
      username: '',
      password: '',
      email: '',
      role: 'user'
    })
    
    const editForm = reactive({
      id: '',
      username: '',
      password: '',
      email: '',
      role: 'user'
    })
    
    // 表单验证规则
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
      ],
      role: [
        { required: true, message: '请选择角色', trigger: 'change' }
      ]
    }
    
    // 计算属性：过滤后的用户列表
    const filteredUsers = computed(() => {
      if (!searchQuery.value) {
        return users.value
      }
      return users.value.filter(user => 
        user.username.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })
    
    // 激活的菜单
    const activeMenu = computed(() => {
      return window.location.pathname
    })
    
    // 加载用户列表
    const loadUsers = async () => {
      try {
        const response = await axios.get('/api/users')
        users.value = response.data
      } catch (err) {
        console.error('加载用户列表失败:', err)
      }
    }
    
    // 搜索用户
    const handleSearch = () => {
      // 搜索逻辑已在计算属性中实现
    }
    
    // 打开新增用户对话框
    const openCreateDialog = () => {
      createDialogVisible.value = true
    }
    
    // 打开编辑用户对话框
    const openEditDialog = (user) => {
      editForm.id = user.id
      editForm.username = user.username
      editForm.email = user.email
      editForm.role = user.role
      editForm.password = ''
      editDialogVisible.value = true
    }
    
    // 打开删除用户对话框
    const openDeleteDialog = (user) => {
      deleteUser.value = user
      deleteDialogVisible.value = true
    }
    
    // 重置新增表单
    const resetCreateForm = () => {
      createForm.username = ''
      createForm.password = ''
      createForm.email = ''
      createForm.role = 'user'
      if (createFormRef.value) {
        createFormRef.value.resetFields()
      }
    }
    
    // 重置编辑表单
    const resetEditForm = () => {
      editForm.password = ''
      if (editFormRef.value) {
        editFormRef.value.clearValidate(['password'])
      }
    }
    
    // 创建用户
    const handleCreate = async () => {
      try {
        await createFormRef.value.validate()
        
        const response = await axios.post('/api/users', createForm)
        await loadUsers()
        createDialogVisible.value = false
        resetCreateForm()
        
        ElMessage.success('用户创建成功')
      } catch (err) {
        console.error('创建用户失败:', err)
        if (err.response) {
          ElMessage.error(err.response.data.message || '创建用户失败')
        } else {
          ElMessage.error('创建用户失败')
        }
      }
    }
    
    // 编辑用户
    const handleEdit = async () => {
      try {
        await editFormRef.value.validate()
        
        // 只发送有变化的字段
        const updateData = {
          email: editForm.email,
          role: editForm.role
        }
        
        if (editForm.password) {
          updateData.password = editForm.password
        }
        
        const response = await axios.put(`/api/users/${editForm.id}`, updateData)
        await loadUsers()
        editDialogVisible.value = false
        resetEditForm()
        
        ElMessage.success('用户编辑成功')
      } catch (err) {
        console.error('编辑用户失败:', err)
        if (err.response) {
          ElMessage.error(err.response.data.message || '编辑用户失败')
        } else {
          ElMessage.error('编辑用户失败')
        }
      }
    }
    
    // 删除用户
    const handleDelete = async () => {
      try {
        const response = await axios.delete(`/api/users/${deleteUser.value.id}`)
        await loadUsers()
        deleteDialogVisible.value = false
        
        ElMessage.success('用户删除成功')
      } catch (err) {
        console.error('删除用户失败:', err)
        if (err.response) {
          ElMessage.error(err.response.data.message || '删除用户失败')
        } else {
          ElMessage.error('删除用户失败')
        }
      }
    }
    
    // 退出登录
    const handleCommand = (command) => {
      if (command === 'logout') {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
    }
    
    // 初始化加载用户列表
    onMounted(() => {
      loadUsers()
    })
    
    return {
      username,
      users,
      searchQuery,
      createDialogVisible,
      editDialogVisible,
      deleteDialogVisible,
      createFormRef,
      editFormRef,
      deleteUser,
      createForm,
      editForm,
      rules,
      filteredUsers,
      activeMenu,
      openCreateDialog,
      openEditDialog,
      openDeleteDialog,
      resetCreateForm,
      resetEditForm,
      handleCreate,
      handleEdit,
      handleDelete,
      handleSearch,
      handleCommand
    }
  }
}
</script>

<style scoped>
.users-container {
  height: 100vh;
}

.users-header {
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

.users-aside {
  background-color: #fff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
}

.aside-menu {
  height: 100%;
  border-right: none;
}

.users-main {
  background-color: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}

.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.main-header h2 {
  color: #333;
  font-size: 1.8rem;
  font-weight: 600;
  margin: 0;
}

.users-card {
  border-radius: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-input {
  width: 200px;
}

.delete-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 20px 0;
}

.warning-icon {
  font-size: 48px;
  color: #e6a23c;
  margin-bottom: 16px;
}

.username-text {
  font-weight: 600;
  color: #f56c6c;
}

.delete-hint {
  color: #909399;
  font-size: 14px;
  margin-top: 8px;
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
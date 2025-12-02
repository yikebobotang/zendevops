<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>部署平台</h2>
        <p>请登录您的账号</p>
      </div>
      
      <el-form 
        :model="loginForm" 
        :rules="rules" 
        ref="loginFormRef"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username" 
            placeholder="请输入用户名" 
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="请输入密码" 
            prefix-icon="Lock"
            show-password
            size="large"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            native-type="submit" 
            :loading="loading"
            block
            size="large"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <el-alert 
        v-if="error" 
        :title="error" 
        type="error" 
        show-icon 
        :closable="false"
        class="error-alert"
      />
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import axios from 'axios'

export default {
  name: 'Login',
  setup() {
    const loginFormRef = ref(null)
    const loading = ref(false)
    const error = ref('')
    
    const loginForm = reactive({
      username: '',
      password: ''
    })
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ]
    }
    
    const handleLogin = async () => {
      try {
        await loginFormRef.value.validate()
        loading.value = true
        error.value = ''
        
        const response = await axios.post('/api/login', loginForm)
        localStorage.setItem('token', response.data.token)
        window.location.href = '/home'
      } catch (err) {
        if (err.response) {
          error.value = err.response.data.message || '登录失败，请检查用户名和密码'
        } else if (err.message) {
          error.value = err.message
        } else {
          error.value = '登录失败，请检查用户名和密码'
        }
      } finally {
        loading.value = false
      }
    }
    
    return {
      loginFormRef,
      loginForm,
      rules,
      loading,
      error,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 420px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h2 {
  color: #333;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.login-header p {
  color: #666;
  font-size: 1rem;
}

.error-alert {
  margin-top: 1rem;
}

:deep(.el-button--primary) {
  background-color: #667eea;
  border-color: #667eea;
}

:deep(.el-button--primary:hover) {
  background-color: #5a6fd8;
  border-color: #5a6fd8;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
}
</style>
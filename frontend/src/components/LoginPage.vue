<template>
    <div class="login-container">
      <h2>管理员登录</h2>
      <form @submit.prevent="login">
        <div>
          <label for="username">用户名:</label>
          <input id="username" v-model="username" type="text" required />
        </div>
        <div>
          <label for="password">密码:</label>
          <input id="password" v-model="password" type="password" required />
        </div>
        <button type="submit">登录</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoginPage',
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      login() {
        if (this.username === 'admin' && this.password === 'admin') {
          this.$router.push('/admin');
          localStorage.setItem('auth', true); // 简单示例，实际应用中请勿这样做
        } else {
          alert('用户名或密码错误！');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 20px;
    box-sizing: border-box;
  }
  
  h2 {
    color: #333;
    margin-bottom: 20px;
  }
  
  form {
    background: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
  }
  
  div {
    margin-bottom: 15px;
    width: 100%;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    color: #333;
  }
  
  input[type="text"], input[type="password"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-sizing: border-box;
  }
  
  button {
    cursor: pointer;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
    width: 100%;
    box-sizing: border-box;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  
  
<template>
  <div class="admin-page">
    <h1>管理页面</h1>
    <!-- 密码验证表单 -->
    <form @submit.prevent="verifyPassword">
      <div>
        <label for="password">管理员密码:</label>
        <input id="password" v-model="adminPassword" type="password" required>
      </div>
      <button type="submit">重置所有投票</button>
    </form>
  </div>
</template>

  
<script>
export default {
  name: 'AdminPage',
  data() {
    return {
      adminPassword: '', // 管理员密码输入
    };
  },
  methods: {
    verifyPassword() {
      const hardcodedPassword = 'admin'; // 硬编码的密码
      if (this.adminPassword === hardcodedPassword) {
        this.clearVotes(); // 密码正确，调用清空投票记录的方法
      } else {
        alert('密码错误');
      }
    },
    clearVotes() {
      // 调用后端接口清空投票记录
      fetch('/api/clear-votes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => {
        alert(data.message); // 显示后端返回的成功信息
      })
      .catch(error => {
        console.error('Error clearing votes:', error);
        alert('清空投票记录过程中出现错误');
      });
    },
  },
};
</script>

  
  
  <style scoped>
  .admin-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 20px;
  }
  
  h1 {
    color: #333;
    margin-bottom: 20px;
  }
  
  button {
    cursor: pointer;
    background-color: #007bff;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
    margin: 5px;
    transition: background-color 0.3s ease;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  form {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 600px;
  }
  
  input[type="text"], select {
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
    border: 1px solid #ddd;
    box-sizing: border-box;
  }
  
  .polls {
    width: 100%;
    max-width: 600px;
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin: 20px 0;
    overflow: hidden;
  }
  
  .poll-item {
    padding: 15px;
    border-bottom: 1px solid #f0f0f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .poll-item:last-child {
    border-bottom: none;
  }
  
  .poll-title {
    font-size: 16px;
  }
  
  .action-buttons {
    display: flex;
    justify-content: flex-end;
  }
  
  .action-button {
    margin-left: 10px;
  }
  </style>
  
  
<template>
    <div class="admin-page">
      <h1>创建新投票</h1>
      <form @submit.prevent="createPoll">
        <div>
          <label for="pollName">投票名称:</label>
          <input id="pollName" v-model="poll.name" type="text" required>
        </div>
        <div v-for="(option, index) in poll.options" :key="index">
          <label for="option">投票选项 {{ index + 1 }}:</label>
          <input v-model="option.title" type="text" required>
          <button @click.prevent="removeOption(index)">移除</button>
        </div>
        <button @click.prevent="addOption">添加选项</button>
        <div>
          <label for="maxVotes">候选人数:</label>
          <input id="maxVotes" v-model.number="poll.maxVotes" type="number" min="1" required>
        </div>
        <button type="submit">创建投票</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AdminPage',
    data() {
      return {
        poll: {
          name: '',
          options: [{ title: '' }, { title: '' }], // 初始时有两个空的投票选项
          maxVotes: 1,
        },
      };
    },
    methods: {
      addOption() {
        this.poll.options.push({ title: '' });
      },
      removeOption(index) {
        this.poll.options.splice(index, 1);
      },
      createPoll() {
        // 这里应该包含将新创建的投票发送到后端的代码
        // 例如：axios.post('/api/polls', this.poll)
        console.log('创建的投票:', this.poll);
        this.resetForm();
      },
      resetForm() {
        this.poll = { name: '', options: [{ title: '' }, { title: '' }], maxVotes: 1 };
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
  
  
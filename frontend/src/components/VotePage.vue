<template>
  <div class="vote-page">
    <h1>请投票</h1>
    <!-- 投票人姓名输入和验证 -->
    <div v-if="!voterVerified">
      <input type="text" v-model="voterName" placeholder="请输入您的姓名" />
      <button @click="verifyVoter">验证</button>
    </div>
    <!-- 投票选项显示 -->
    <div v-if="voterVerified">
      <p>请选择最多{{ maxVotes }}位候选人</p>
      <div v-for="option in polls" :key="option.id" class="poll-option">
        <input type="checkbox" :value="option" v-model="selectedOptions" :disabled="selectedOptions.length >= maxVotes && !selectedOptions.includes(option)">
        {{ option.title }}
      </div>
      <button @click="submitVote">提交投票</button>
    </div>
    <!-- 投票结果显示 -->
    <div v-if="showResults">
      <h2>投票结果</h2>
      <div v-for="result in voteResults" :key="result.id" class="vote-result">
        {{ result.title }}: {{ result.votes }}票
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VotePage',
  data() {
    return {
      voterName: '', // 投票人姓名
      voterVerified: false, // 标记投票人是否已验证
      polls: [
        // 静态投票选项数据
        { id: 1, title: '候选项1' },
        { id: 2, title: '候选项2' },
        // 可以根据需要添加更多选项
      ],
      selectedOptions: [], // 用户选中的投票选项
      maxVotes: 1, // 从后端获取的候选人数限制（暂时使用静态数据）
      voteResults: [], // 投票结果
      showResults: false, // 是否显示投票结果
    };
  },
  methods: {
    // 验证投票人姓名
    verifyVoter() {
      // 这里暂时使用静态验证逻辑，只有姓名为"ZZZ"时验证通过
      if (this.voterName === 'ZZZ') {
        this.voterVerified = true;
      } else {
        alert('姓名验证失败');
      }
    },
    // 提交投票
    submitVote() {
      // 这里应包含将投票结果发送到后端的逻辑，暂时使用静态数据模拟
      this.voteResults = this.selectedOptions.map(option => ({
        id: option.id,
        title: option.title,
        votes: 1, // 在真实应用中，这应该是根据后端统计的结果
      }));
      this.showResults = true; // 显示投票结果
      this.selectedOptions = []; // 清空已选选项，以便下一次投票
    },
  },
};
</script>
  
  <style scoped>
  .vote-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: #F0F4F8; /* 使用更加柔和的背景色 */
    padding: 20px;
    box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* 现代且易读的字体 */
  }
  
  h1, h2 {
    color: #333;
    margin: 20px 0;
  }
  
  input[type="text"] {
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #D3D3D3; /* 细致的边框 */
    border-radius: 5px;
    width: 300px; /* 调整输入框宽度 */
    outline: none; /* 移除焦点轮廓 */
  }
  
  button {
    cursor: pointer;
    background-color: #007AFF; /* 鲜艳的按钮颜色 */
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
    transition: background-color 0.3s, transform 0.2s;
    outline: none;
  }
  
  button:hover {
    background-color: #0056b3;
    transform: scale(1.05); /* 轻微的放大效果 */
  }
  
  .poll-option, .vote-result {
    background-color: #ffffff;
    padding: 15px;
    margin: 10px 0;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 添加轻微的阴影以提升层次感 */
    width: 80%;
    text-align: left; /* 左对齐文本 */
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  input[type="checkbox"] {
    margin-right: 10px;
  }
  
  .vote-result {
    justify-content: flex-start;
  }
  </style>
  
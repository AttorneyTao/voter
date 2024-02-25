<template>
  <div class="vote-page">
    <h1>{{ pageTitle }}</h1>
    <div v-if="!voterVerified && !pollId">
      <input type="text" v-model="voterName" placeholder="请输入您的姓名" />
      <button @click="verifyVoter">验证</button>
     
     </div>
<div v-if="!voterVerified && !pollId"> 
  <!-- 下拉列表选择轮次 -->
  <select v-model="selectedPollId">
    <option disabled value="">请选择轮次</option>
    <option v-for="round in allRounds" :key="round" :value="round">轮次 {{ round }}</option>
  </select>
    <!-- 查看选定轮次的结果 -->
  <button @click="viewSelectedRoundResults">查看结果</button>
</div>
      

    <!-- 投票轮次选择 -->
    <div v-if="voterVerified && !pollId">
      <button v-for="round in rounds" :key="round" @click="selectRound(round)">第 {{ round }} 轮投票</button>
    </div>
<!-- 投票选项显示 -->
<div v-if="pollId && !showResults">
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
  <div v-for="result in voteResults" :key="result.option_id" class="vote-result">
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
      pageTitle: '请输入您的姓名',
      voterName: '', // 投票人姓名
      voterVerified: false, // 标记投票人是否已验证
      pollId: null, // 当前选择的投票轮次ID
      rounds: [1, 2, 3], // 可用的投票轮次
      polls: [], // 动态加载的投票选项数据
      selectedOptions: [], // 用户选中的投票选项
      maxVotes: 1, // 从后端获取的候选人数限制
      voteResults: [], // 投票结果
      showResults: false, // 是否显示投票结果
      allPollsResults: [],
      allRounds: [1, 2, 3], 
    };
  },
  methods: {
    verifyVoter() {
      // 向后端发送请求，验证投票人姓名
      fetch('/api/verify-voter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ voterName: this.voterName })
      })
      .then(response => {
        if (!response.ok) throw new Error('验证失败');
        return response.json();
      })
      .then(data => {
        if (data.verified) {
          this.voterVerified = true;
          this.pageTitle = '请选择投票轮次';
          this.showResults = false;
        } else {
          alert('姓名验证失败');
        }
      })
      .catch(error => {
        console.error('Error verifying voter:', error);
        alert('验证过程中出现错误');
      });
    },
    viewSelectedRoundResults() {
    if (this.selectedPollId) {
      this.fetchVoteResults(this.selectedPollId); // 获取并显示选定轮次的投票结果
    } else {
      alert('请选择一个轮次');
    }
  },
  
  selectRound(pollId) {
    // 验证用户是否已经投票
    fetch('/api/has-voted', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ voterName: this.voterName, pollId: pollId })
    })
    .then(response => response.json())
    .then(data => {
      if (data.hasVoted) {
        // 如果用户已经投票，则显示投票结果
        this.fetchVoteResults(pollId); // 假设这个方法用于获取并显示投票结果
      } else {
        // 如果用户未投票，则加载投票选项
        this.fetchPollOptions(pollId);
        this.pollId = pollId; // 保存当前轮次ID
      }
    })
    .catch(error => console.error('Error checking if voter has voted:', error));
  },

  fetchPollOptions(pollId) {
  fetch(`/api/polls/${pollId}`)
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => {
      this.polls = data.poll.options; // 使用后端返回的选项数据
      this.maxVotes = data.poll.max_votes; // 使用后端返回的最大投票数
      this.showResults = false; // 确保不显示投票结果
      this.pageTitle= data.poll.title;
    })
    .catch(error => console.error('Error fetching poll options:', error));
},


fetchVoteResults(pollId) {
  fetch(`/api/poll-results/${pollId}`)
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => {
      this.voteResults = data.results; // 使用后端返回的投票结果数据
      this.showResults = true; // 显示投票结果
    })
    .catch(error => console.error('Error fetching vote results:', error));
},



submitVote() {
  fetch('/api/vote', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      voterName: this.voterName,
      selectedOptions: this.selectedOptions.map(option => option.id),
      pollId: this.pollId
    })
  })
  .then(response => {
    if (!response.ok) throw new Error('Network response was not ok');
    return response.json();
  })
  .then(() => { // 移除了未使用的参数 `data`
    alert('投票成功'); // 显示投票成功的弹窗
    this.fetchVoteResults(this.pollId); // 获取并显示当前投票结果
    this.selectedOptions = []; // 清空已选选项，以便下一次投票
  })
  .catch(error => {
    console.error('Error submitting vote:', error);
    alert('提交投票过程中出现错误');
  });
},
viewAllResultsDirectly() {
    this.allPollsResults = []; // 清空之前的结果
    this.showResults = true; // 显示结果部分

    // 假设`rounds`数组存储了所有轮次的ID
    this.rounds.forEach((pollId) => {
      fetch(`/api/poll-results/${pollId}`)
        .then(response => {
          if (!response.ok) throw new Error('Network response was not ok');
          return response.json();
        })
        .then(data => {
          this.allPollsResults.push({
            pollTitle: `轮次 ${pollId} 结果`, // 假设您需要根据pollId生成轮次标题
            options: data.results, // 使用后端返回的投票结果数据
          });
        })
        .catch(error => console.error(`Error fetching results for poll ${pollId}:`, error));
    });
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
  
<template>
  <div id="app" class="timesheet-container">
    <header class="header">
      <h1>🕒 Timesheet 智能工时管理平台</h1>
      <p class="user-info">当前用户: <strong>Alexxxu</strong> (Network Engineer)</p>
    </header>

    <main class="main-content">
      <section class="card form-card">
        <h2>📊 录入今日工时</h2>
        <div class="form-group">
          <label>选择关联项目/工单</label>
          <select v-model="form.ticket">
            <option value="" disabled>-- 请选择工单 --</option>
            <option value="ticket-01">Core-Switch-Migration (核心交换机割接)</option>
            <option value="ticket-02">SD-WAN-Deployment (SD-WAN 部署维护)</option>
            <option value="ticket-03">Firewall-Policy-Audit (防火墙策略审计)</option>
          </select>
        </div>

        <div class="form-group">
          <label>投入工时 (Hours)</label>
          <input type="number" v-model.number="form.hours" min="0.5" max="24" step="0.5" placeholder="请输入小时数，如 4.5">
        </div>

        <div class="form-group">
          <label>工作内容描述</label>
          <textarea v-model="form.description" placeholder="请简要写下今天跟进的技术进展..."></textarea>
        </div>

        <button @click="submitTimesheet" class="btn-submit">确认提交工时</button>
      </section>

      <section class="card status-card">
        <h2>📅 今日工时看板</h2>
        <div class="dashboard-grid">
          <div class="metric-box">
            <span class="label">今日已报</span>
            <span class="value">{{ totalHours }} 小时</span>
          </div>
          <div class="metric-box status-ok">
            <span class="label">系统状态</span>
            <span class="value text-success">DB / API 在线</span>
          </div>
        </div>

        <div class="history-list">
          <h3>📋 今日提交记录</h3>
          <div v-if="records.length === 0" class="empty-tip">暂无提交记录，请在左侧录入。</div>
          <ul v-else>
            <li v-for="(item, index) in records" :key="index">
              <span class="time">⏱️ {{ item.hours }}h</span>
              <span class="desc"><strong>[{{ item.ticket }}]</strong> {{ item.description }}</span>
            </li>
          </ul>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      form: { ticket: '', hours: '', description: '' },
      records: []
    }
  },
  computed: {
    totalHours() {
      return this.records.reduce((sum, item) => sum + item.hours, 0);
    }
  },
  methods: {
    submitTimesheet() {
      if (!this.form.ticket || !this.form.hours || !this.form.description) {
        alert('请把表单填写完整再提交哦！');
        return;
      }
      if (this.form.hours > 24 || this.form.hours <= 0) {
        alert('单次申报工时必须在 0 到 24 小时之间！');
        return;
      }
      
      // 压入本地历史列表（模拟前端交互效果）
      this.records.push({ ...this.form });
      alert(`工时提交成功！成功为 ${this.form.ticket} 录入 ${this.form.hours} 小时。`);
      
      // 清空表单
      this.form.ticket = '';
      this.form.hours = '';
      this.form.description = '';
    }
  }
}
</script>

<style scoped>
.timesheet-container { font-family: 'Segoe UI', system-ui, sans-serif; background-color: #f4f6f9; color: #333; min-height: 100vh; padding: 20px; }
.header { background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 25px; }
.header h1 { margin: 0; font-size: 24px; }
.user-info { margin: 5px 0 0 0; font-size: 14px; opacity: 0.9; }
.main-content { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; max-width: 1200px; margin: 0 auto; }
.card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid #e5e7eb; }
.card h2 { margin-top: 0; margin-bottom: 20px; font-size: 18px; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; display: inline-block; }
.form-group { margin-bottom: 18px; }
.form-group label { display: block; font-weight: 600; margin-bottom: 6px; font-size: 14px; color: #4b5563; }
.form-group select, .form-group input, .form-group textarea { width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; box-sizing: border-box; font-size: 14px; }
.form-group textarea { height: 80px; resize: none; }
.btn-submit { width: 100%; background-color: #2563eb; color: white; border: none; padding: 12px; border-radius: 6px; font-size: 15px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
.btn-submit:hover { background-color: #1d4ed8; }
.dashboard-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
.metric-box { background: #f3f4f6; padding: 15px; border-radius: 8px; text-align: center; }
.metric-box .label { display: block; font-size: 12px; color: #6b7280; margin-bottom: 5px; }
.metric-box .value { font-size: 20px; font-weight: 700; color: #111827; }
.status-ok { background: #f0fdf4; }
.text-success { color: #16a34a !important; }
.history-list h3 { font-size: 14px; color: #4b5563; margin-bottom: 10px; }
.empty-tip { text-align: center; color: #9ca3af; font-size: 13px; padding: 20px 0; }
.history-list ul { list-style: none; padding: 0; margin: 0; }
.history-list li { display: flex; align-items: center; padding: 10px; background: #f9fafb; border-radius: 6px; margin-bottom: 8px; border-left: 4px solid #3b82f6; font-size: 13px; }
.history-list .time { font-weight: bold; color: #2563eb; margin-right: 12px; white-space: nowrap; }
</style>
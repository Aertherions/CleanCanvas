<template>
  <div>
    <section class="hero-grid">
      <div>
        <span class="eyebrow fade-up">MVP · 免费可跑通版本</span>
        <h1 class="fade-up delay-1">AI Content Studio for Clean Creation</h1>
        <p class="lead fade-up delay-2">
          上传图片或视频，选择素材修复、图片压缩、视频任务等工具，用积分计费完成生成结果。多平台发布能力已预留，后续通过官方 API 接入。
        </p>
        <div class="actions fade-up delay-3">
          <RouterLink class="button primary" to="/signup">开始使用</RouterLink>
          <RouterLink class="button secondary" to="/upload">上传素材</RouterLink>
        </div>
      </div>
      <div class="preview-card fade-up delay-4">
        <span class="eyebrow">Workspace preview</span>
        <div class="grid" style="margin-top:18px">
          <div class="metric">
            <span class="muted">当前积分</span>
            <strong>1,000</strong>
          </div>
          <div class="progress"><span style="width:72%"></span></div>
          <div class="grid cols-3">
            <div class="card"><h3>素材修复</h3><p class="muted">授权素材内容清理</p></div>
            <div class="card"><h3>图片压缩</h3><p class="muted">小图片可演示</p></div>
            <div class="card"><h3>任务中心</h3><p class="muted">进度与结果</p></div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <h2>核心流程</h2>
        <p class="muted">上传素材 → 选择工具 → 消耗积分 → 生成结果 → 下载或发布</p>
      </div>
      <div class="grid cols-4">
        <div v-for="step in steps" :key="step" class="card fade-up">
          <span class="eyebrow">{{ step }}</span>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <h2>MVP 功能入口</h2>
        <p class="muted">第一版只做免费可跑通版本，真实支付和视频处理后续接入。</p>
      </div>
      <div class="grid cols-3">
        <RouterLink v-for="item in tools" :key="item.to" class="card" :to="item.to">
          <h3>{{ item.title }}</h3>
          <p class="muted">{{ item.desc }}</p>
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const steps = ['上传素材', '选择工具', '消耗积分', '生成结果', '下载或发布']
const tools = [
  { title: '用户中心', desc: '查看积分、订单、任务和文件。', to: '/dashboard' },
  { title: '充值中心', desc: '创建 mock 充值订单并增加积分。', to: '/recharge' },
  { title: '图片工具', desc: '图片压缩、封面裁剪、图片修复。', to: '/image-tools' },
  { title: '视频工具', desc: '演示视频压缩、裁剪、转换和修复任务。', to: '/video-tools' },
  { title: '任务中心', desc: '查看 queued / processing / success 等状态。', to: '/tasks' },
  { title: '多平台发布', desc: 'YouTube、TikTok、B站、抖音等官方 API 预留。', to: '/publish' },
]
</script>

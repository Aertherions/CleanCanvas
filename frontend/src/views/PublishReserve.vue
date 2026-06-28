<template>
  <div class="stack fade-up">
    <div>
      <span class="eyebrow">Publishing reserve</span>
      <h2 style="margin-top:12px">多平台发布预留</h2>
      <p class="lead">
        多平台发布功能已预留，后续将通过官方 API 接入。当前版本暂不开放真实发布。
      </p>
    </div>
    <div class="grid cols-4">
      <div v-for="platform in platforms" :key="platform" class="card">
        <h3>{{ platform }}</h3>
        <p class="muted">官方 API 预留</p>
      </div>
    </div>
    <div class="notice">
      禁止使用抓包、模拟登录、逆向接口、绕过平台审核等方式接入平台。后续只通过平台公开、合规、官方 API 实现。
    </div>
  </div>
</template>

<script setup>
const platforms = ['YouTube', 'TikTok', 'Instagram', 'Facebook', 'X', 'B站', '快手', '小红书', '抖音']
</script>

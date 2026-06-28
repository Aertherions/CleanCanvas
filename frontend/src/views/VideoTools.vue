<template>
  <ToolPage
    title="视频工具"
    eyebrow="Video tools"
    note="当前为演示任务，真实视频处理将在服务器版本开放。禁止抓包、模拟登录、逆向接口或绕过平台审核。"
    :tools="tools"
    file-type="video"
  />
</template>

<script setup>
import ToolPage from './ToolPage.vue'

const tools = [
  { type: 'video_compress', name: '视频压缩', cost: 30 },
  { type: 'video_crop', name: '视频裁剪', cost: 30 },
  { type: 'video_convert', name: '格式转换', cost: 30 },
  { type: 'video_repair', name: '自有素材水印修复', cost: 30 },
]
</script>

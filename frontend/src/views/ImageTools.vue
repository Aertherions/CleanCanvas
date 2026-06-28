<template>
  <ToolPage
    title="图片工具"
    eyebrow="Image tools"
    note="图片压缩可演示生成结果；封面裁剪、图片修复、自有素材水印修复第一版为 mock 任务。"
    :tools="tools"
    file-type="image"
  />
</template>

<script setup>
import ToolPage from './ToolPage.vue'

const tools = [
  { type: 'image_compress', name: '图片压缩', cost: 10 },
  { type: 'cover_crop', name: '封面裁剪', cost: 5 },
  { type: 'image_repair', name: '图片瑕疵修复', cost: 20 },
  { type: 'own_watermark_repair', name: '自有素材水印修复', cost: 20 },
]
</script>

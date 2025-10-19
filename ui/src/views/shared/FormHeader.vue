<template>
  <div class="bg-white rounded-lg shadow-sm">
    <div class="bg-gradient-primary text-white p-5 rounded-t-lg">
      <h3 class="text-2xl font-bold">{{ title }}</h3>
    </div>
  </div>
</template>

<script setup lang="ts">
const { title } = defineProps<{ title: string }>();
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>

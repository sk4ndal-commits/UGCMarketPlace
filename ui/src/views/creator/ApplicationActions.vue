<template>
  <div class="flex gap-2">
    <button @click="$emit('edit')" class="px-3 py-1.5 bg-blue-500 text-white rounded">Edit</button>
    <button @click="$emit('delete')" class="px-3 py-1.5 bg-red-500 text-white rounded">Delete</button>
  </div>
</template>

<script setup lang="ts">
// simple action component
</script>

<style scoped></style>

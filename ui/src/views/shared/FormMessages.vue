<template>
  <div>
    <div v-if="successMessage" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4 flex justify-between items-center">
      {{ successMessage }}
      <button type="button" class="text-green-700 hover:text-green-900 font-bold text-xl" @click="$emit('clear-success')">&times;</button>
    </div>

    <div v-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 flex justify-between items-center">
      {{ errorMessage }}
      <button type="button" class="text-red-700 hover:text-red-900 font-bold text-xl" @click="$emit('clear-error')">&times;</button>
    </div>
  </div>
</template>

<script setup lang="ts">
const { successMessage, errorMessage } = defineProps<{ successMessage: string; errorMessage: string }>();
const emits = defineEmits(['clear-success','clear-error']);
</script>

<style scoped></style>

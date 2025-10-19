<template>
  <div class="mb-4">
    <label for="parameters" class="block text-sm font-medium text-gray-700 mb-1">
      Parameters (JSON format)
    </label>
    <textarea
      id="parameters"
      class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
      :class="errors.parameters ? 'border-red-500' : 'border-gray-300'"
      :value="parametersJson"
      @input="onInput"
      rows="4"
      placeholder='{"key": "value"}'
    ></textarea>
    <div v-if="errors.parameters" class="text-red-600 text-sm mt-1">{{ errors.parameters }}</div>
    <p class="text-xs text-gray-500 mt-1">Leave empty for no parameters or enter valid JSON</p>
  </div>
</template>

<script setup lang="ts">
const { parametersJson, errors } = defineProps<{
  parametersJson: string;
  errors: Record<string, string>;
}>();

const emits = defineEmits<{ (e: 'update:parametersJson', value: string): void }>();

function onInput(e: Event) {
  const t = e.target as HTMLTextAreaElement;
  emits('update:parametersJson', t.value);
}
</script>

<style scoped></style>

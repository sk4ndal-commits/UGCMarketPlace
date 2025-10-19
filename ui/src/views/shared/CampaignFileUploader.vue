<template>
  <div class="mb-4">
    <label for="files" class="block text-sm font-medium text-gray-700 mb-1">Reference Materials (Optional)</label>
    <input id="files" type="file" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" :class="errors.reference_files ? 'border-red-500' : 'border-gray-300'" @change="onChange" multiple accept=".pdf,.jpg,.jpeg,.png,.doc,.docx,.mp4,.mov" />
    <div v-if="errors.reference_files" class="text-red-600 text-sm mt-1">{{ errors.reference_files }}</div>
    <small class="text-gray-500 text-sm block mt-1">Max 10 MB per file. Accepted formats: PDF, JPG, PNG, DOC, DOCX, MP4, MOV</small>

    <div v-if="selectedFiles.length > 0" class="mt-3">
      <strong class="text-sm">Selected files:</strong>
      <ul class="mt-2 space-y-2">
        <li v-for="(file, index) in selectedFiles" :key="index" class="flex justify-between items-center p-3 bg-gray-50 border border-gray-200 rounded">
          <span class="text-sm">{{ file.name }} ({{ formatFileSize(file.size) }})</span>
          <button type="button" class="px-2 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700 transition-colors" @click.prevent="remove(index)">Remove</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ selectedFiles: File[]; errors: Record<string,string> }>();
const emits = defineEmits<{ (e: 'update:selectedFiles', v: File[]): void }>();

function onChange(e: Event) {
  const t = e.target as HTMLInputElement;
  if (!t.files) return;
  const files = Array.from(t.files);
  const maxSize = 10 * 1024 * 1024;
  const invalid = files.filter(f => f.size > maxSize);
  if (invalid.length > 0) {
    emits('update:selectedFiles', props.selectedFiles);
    return;
  }
  emits('update:selectedFiles', [...props.selectedFiles, ...files]);
}

function remove(index: number) {
  const copy = [...props.selectedFiles];
  copy.splice(index, 1);
  emits('update:selectedFiles', copy);
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
</script>

<style scoped></style>

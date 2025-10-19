<template>
  <div class="space-y-4">
    <ApplicationItem
      v-for="app in applications"
      :key="app.id"
      :app="app"
      :isCreator="true"
      :currentUserId="currentUserId"
      @view="$emit('view', $event)"
      @edit="$emit('edit', $event)"
      @deleted="$emit('deleted', $event)"
    />
  </div>
</template>

<script setup lang="ts">
import ApplicationItem from './ApplicationItem.vue';
const props = defineProps<{ applications: any[]; currentUserId?: number | null }>();
const emits = defineEmits(['view', 'edit', 'deleted']);
const { applications, currentUserId } = props;
</script>

<style scoped></style>

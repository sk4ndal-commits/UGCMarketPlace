<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <CampaignCard
      v-for="campaign in campaigns"
      :key="campaign.id"
      :campaign="campaign"
      :isBrand="isBrand"
      @view="$emit('view', $event)"
      @edit="$emit('edit', $event)"
      @delete="$emit('delete', $event)"
    />
  </div>
</template>

<script setup lang="ts">
import type { Campaign } from '../../models/campaign';
import CampaignCard from './CampaignCard.vue';
const { campaigns, isBrand } = defineProps<{ campaigns: Campaign[]; isBrand: boolean }>();
const emits = defineEmits(['view', 'edit', 'delete']);
</script>

<style scoped></style>

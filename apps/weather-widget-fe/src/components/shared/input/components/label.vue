<template>
  <label :for="forId" :class="['label', { 'label--required': required }]">
    <slot />
    <span v-if="required" class="label__asterisk">*</span>
  </label>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

const props = defineProps({
  forId: {
    type: String,
    required: false,
    default: '',
  },
  required: {
    type: Boolean,
    default: false,
  },
});
</script>

<style scoped>
.label {
  font-weight: 500;
  font-size: 1em;
  color: #333;
  margin-bottom: 0.25em;
  display: inline-block;
}
.label--required .label__asterisk {
  color: #d32f2f;
  margin-left: 0.2em;
  font-size: 1em;
}
</style>

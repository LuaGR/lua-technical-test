<template>
  <span v-if="message" class="error-message" role="alert">
    <slot>{{ message }}</slot>
  </span>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

defineProps({
  message: {
    type: String,
    default: '',
  },
});
</script>

<style scoped>
.error-message {
  color: #d32f2f;
  font-size: 0.95em;
  margin-top: 0.1em;
  display: block;
}
</style>

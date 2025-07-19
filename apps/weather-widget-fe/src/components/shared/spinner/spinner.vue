<template>
  <span
    class="spinner"
    :style="{ width: sizePx, height: sizePx, borderWidth: borderPx }"
    :aria-label="ariaLabel"
    role="status"
  />
</template>

<script setup lang="ts">
import { computed, defineProps } from 'vue';

const props = defineProps({
  size: {
    type: [Number, String],
    default: 24,
  },
  border: {
    type: [Number, String],
    default: 3,
  },
  ariaLabel: {
    type: String,
    default: 'Cargando',
  },
});

const sizePx = computed(() =>
  typeof props.size === 'number' ? `${props.size}px` : props.size
);
const borderPx = computed(() =>
  typeof props.border === 'number' ? `${props.border}px` : props.border
);
</script>

<style scoped>
.spinner {
  display: inline-block;
  border-radius: 50%;
  border-style: solid;
  border-color: #1976d2 transparent #1976d2 transparent;
  animation: spin 0.8s linear infinite;
  vertical-align: middle;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>

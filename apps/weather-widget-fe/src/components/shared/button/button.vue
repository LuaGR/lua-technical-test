<template>
  <button
    :type="type"
    :class="computedClass"
    :disabled="disabled || loading"
    @click="onClick"
  >
    <span v-if="loading" class="spinner"></span>
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed, defineProps, defineEmits } from 'vue';

const props = defineProps({
  type: {
    type: String as () => 'button' | 'submit' | 'reset',
    default: 'button',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  variant: {
    type: String,
    default: 'primary',
  },
});

const emit = defineEmits(['click']);

const computedClass = computed(() => [
  'btn',
  `btn--${props.variant}`,
  { 'btn--disabled': props.disabled || props.loading },
]);

function onClick(event: MouseEvent) {
  if (!props.disabled && !props.loading) {
    emit('click', event);
  }
}
</script>

<style scoped>
.btn {
  padding: 0.8em 1.8em;
  border-radius: 4px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  background: #1976d2;
  color: #fff;
}
.btn--secondary {
  background: #e0e0e0;
  color: #333;
}
.btn--disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.spinner {
  display: inline-block;
  width: 1em;
  height: 1em;
  border: 2px solid #fff;
  border-top: 2px solid #1976d2;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 0.5em;
  vertical-align: middle;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>

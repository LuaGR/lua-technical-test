<template>
  <span
    class="icon"
    :class="`icon--${name}`"
    :style="{ fontSize: sizePx, color }"
    aria-hidden="true"
  >
    <component :is="iconComponent" />
  </span>
</template>

<script setup lang="ts">
import { computed, defineProps } from 'vue';
import type { Component } from 'vue';
import { SunIcon, CloudIcon, RainIcon, ErrorIcon } from './components';
const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  size: {
    type: [Number, String],
    default: 24,
  },
  color: {
    type: String,
    default: '#1976d2',
  },
});

const sizePx = computed(() =>
  typeof props.size === 'number' ? `${props.size}px` : props.size
);

const icons: Record<string, Component> = {
  sun: SunIcon,
  cloud: CloudIcon,
  rain: RainIcon,
  error: ErrorIcon,
};

const iconComponent = computed(() => icons[props.name] || ErrorIcon);
</script>

<style scoped>
.icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  line-height: 1;
}
</style>

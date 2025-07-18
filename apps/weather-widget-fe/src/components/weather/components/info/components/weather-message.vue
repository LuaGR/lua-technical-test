<template>
  <div class="weather-message">{{ message }}</div>
</template>

<script setup lang="ts">
import { computed, defineProps } from 'vue';

const props = defineProps({
  temperature: { type: [String, Number], required: true },
});

const message = computed(() => {
  const temp = Number(props.temperature);
  if (isNaN(temp)) return '';
  if (temp < 10) return 'It’s cold 🧥';
  if (temp <= 25) return 'Mild weather 🌤';
  return 'It’s hot ☀️';
});
</script>

<style scoped>
.weather-message {
  font-size: 1.1em;
  margin-top: 0.3em;
  font-weight: 500;
}
</style>

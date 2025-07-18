<template>
  <div class="weather-info">
    <Icon :name="icon" :size="48" :color="iconColor" />
    <div class="weather-info__main">
      <div class="weather-info__temp">{{ temperature }}°C</div>
      <div class="weather-info__city">{{ city }}</div>
      <div class="weather-info__desc">{{ description }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, computed } from 'vue';
import { Icon } from '../../shared';
import { WeatherInfo } from '../models/weather.model';

const props = defineProps<WeatherInfo>();

const iconColor = computed(() => {
  const temp = Number(props.temperature);
  if (isNaN(temp)) return '#1976d2';
  if (temp >= 30) return '#e65100';
  if (temp >= 20) return '#fbc02d';
  if (temp >= 10) return '#1976d2';
  return '#0288d1';
});
</script>

<style scoped>
.weather-info {
  display: flex;
  align-items: center;
  gap: 1.5em;
  padding: 1em 0;
}
.weather-info__main {
  display: flex;
  flex-direction: column;
  gap: 0.2em;
}
.weather-info__temp {
  font-size: 2.2em;
  font-weight: bold;
}
.weather-info__city {
  font-size: 1.1em;
  color: #1976d2;
}
.weather-info__desc {
  font-size: 1em;
  color: #757575;
}
</style>

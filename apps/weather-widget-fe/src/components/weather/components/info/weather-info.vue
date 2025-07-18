<template>
  <div class="weather-info">
    <div class="weather-info__main">
      <Icon
        :name="icon"
        :size="56"
        :color="iconColor"
        class="weather-info__icon"
      />
      <div class="weather-info__temp">{{ temperature }}°C</div>
      <div class="weather-info__city">
        {{ city }}
      </div>
      <div class="weather-info__desc">
        {{ description }}
      </div>
    </div>
    <div class="weather-info__message">
      <WeatherMessage :temperature="temperature" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, computed } from 'vue';
import { Icon } from '../../../shared';
import { WeatherInfo } from '../../models/weather.model';
import WeatherMessage from './components/weather-message.vue';

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
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
  width: 100%;
}

.weather-info__main {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3em;
  width: 100%;
}

.weather-info__icon {
  margin-bottom: 0.2em;
}

.weather-info__temp {
  font-size: 2.5em;
  font-weight: bold;
  text-align: center;
}

.weather-info__city {
  font-size: 1.3em;
  font-weight: 500;
  text-align: center;
}

.weather-info__desc {
  font-size: 1.1em;
  color: #555;
  text-align: center;
}

.weather-info__message {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 1.2em;
}

.weather-info__message .weather-message {
  font-size: 2em !important;
  font-weight: 600 !important;
  text-align: center;
  color: #1976d2;
}
</style>

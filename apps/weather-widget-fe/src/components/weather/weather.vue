<template>
  <section class="weather-widget">
    <WeatherForm
      v-model:city="city"
      :loading="loading"
      :error="error"
      @submit="onSubmit"
    />

    <div class="weather-widget__feedback">
      <Spinner v-if="loading" :size="32" />
      <ErrorMessage v-else-if="error" :message="error" />
    </div>

    <WeatherInfo
      v-if="weather"
      :city="weather.city"
      :temperature="weather.temperature"
      :description="weather.description"
      :icon="weather.icon"
    />
  </section>
</template>

<script setup lang="ts">
import { useWeather } from './composables/use-weather.composable';
import { Spinner, ErrorMessage } from '../shared';
import { WeatherForm, WeatherInfo } from './components';

const { city, weather, loading, error, fetchWeather } = useWeather();

function onSubmit() {
  if (city.value && !loading.value) {
    fetchWeather(city.value);
  }
}
</script>

<style scoped>
.weather-widget {
  max-width: 350px;
  margin: 2em auto;
  padding: 2em 1.5em;
  border-radius: 12px;
  background: #f7fafd;
  box-shadow: 0 2px 12px 0 #0001;
  display: flex;
  flex-direction: column;
  gap: 1.5em;
}
.weather-widget__feedback {
  min-height: 2em;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

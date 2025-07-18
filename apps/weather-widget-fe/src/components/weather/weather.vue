<template>
  <div class="weather-widget__page">
    <Header>
      <h1>Weather Widget</h1>
    </Header>

    <div class="weather-widget__center">
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
    </div>
  </div>
</template>

<script setup lang="ts">
import { useWeather } from './composables/use-weather.composable';
import { Spinner, ErrorMessage, Header } from '../shared';
import { WeatherForm, WeatherInfo } from './components';

const { city, weather, loading, error, fetchWeather } = useWeather();

function onSubmit() {
  if (city.value && !loading.value) {
    fetchWeather(city.value);
  }
}
</script>

<style scoped>
.weather-widget__page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding-top: 3.5em;
  padding-bottom: 2.5em;
  box-sizing: border-box;
}

.weather-widget__center {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.weather-widget {
  max-width: 500px;
  width: 100%;
  margin: 0;
  padding: 3em 2em;
  border-radius: 16px;
  background: #f7fafd;
  box-shadow: 0 4px 24px 0 #0002;
  display: flex;
  flex-direction: column;
  gap: 2em;
}
.weather-widget__feedback {
  min-height: 2em;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

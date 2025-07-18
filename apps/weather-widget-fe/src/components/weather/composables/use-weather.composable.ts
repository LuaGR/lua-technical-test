import { ref } from 'vue';
import { WeatherInfo } from '../models/weather.model';
import {
  fetchFromOpenWeather,
  fetchFromFallback,
} from '../../../services/weather.service';

export function useWeather() {
  const loading = ref(false);
  const error = ref<string | null>(null);
  const weather = ref<WeatherInfo | null>(null);
  const city = ref('');

  async function fetchWeather(cityName: string) {
    loading.value = true;
    error.value = null;
    weather.value = null;

    try {
      try {
        weather.value = await fetchFromOpenWeather(cityName);
        return;
      } catch (e) {
        console.error('Error fetching from OpenWeatherMap, using fallback:', e);
      }

      try {
        weather.value = await fetchFromFallback(cityName);
      } catch (e) {
        error.value = "Can't fetch weather data. Please try again later.";
      }
    } finally {
      loading.value = false;
    }
  }

  return {
    loading,
    error,
    weather,
    city,
    fetchWeather,
  };
}

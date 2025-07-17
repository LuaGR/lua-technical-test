import { ref } from 'vue';
import { WeatherInfo } from '../models/weather.model';

const OPENWEATHER_API_KEY = import.meta.env.VITE_OPENWEATHER_API_KEY;
const OPENWEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather';
const FALLBACK_URL = 'https://wttr.in';

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
      const res = await fetch(
        `${OPENWEATHER_URL}?q=${encodeURIComponent(
          cityName
        )}&appid=${OPENWEATHER_API_KEY}&units=metric&lang=es`
      );
      if (!res.ok) throw new Error('No se encontró la ciudad');
      const data = await res.json();
      weather.value = {
        city: data.name,
        temperature: Math.round(data.main.temp),
        description: data.weather[0].description,
        icon: mapWeatherToIcon(data.weather[0].main),
      };
      return;
    } catch (e) {
      console.error('Error al consultar OpenWeatherMap, usando fallback:', e);
    }

    try {
      const res = await fetch(
        `${FALLBACK_URL}/${encodeURIComponent(cityName)}?format=j1`
      );
      if (!res.ok) throw new Error('No se encontró la ciudad');
      const data = await res.json();
      weather.value = {
        city: cityName,
        temperature: Math.round(Number(data.current_condition[0].temp_C)),
        description: data.current_condition[0].weatherDesc[0].value,
        icon: mapWeatherToIcon(data.current_condition[0].weatherDesc[0].value),
      };
    } catch (e) {
      error.value = 'No se pudo obtener el clima. Intenta con otra ciudad.';
    } finally {
      loading.value = false;
    }
  }

  function mapWeatherToIcon(desc: string): string {
    const d = desc.toLowerCase();
    if (d.includes('rain') || d.includes('lluvia')) return 'rain';
    if (d.includes('cloud') || d.includes('nube')) return 'cloud';
    if (d.includes('sun') || d.includes('sol')) return 'sun';
    if (d.includes('clear') || d.includes('despejado')) return 'sun';
    return 'cloud';
  }

  return {
    loading,
    error,
    weather,
    city,
    fetchWeather,
  };
}

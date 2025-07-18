import { WeatherInfo } from '../components/weather/models/weather.model';
import { mapWeatherToIcon } from '../utils/weather-map-icon';

const OPENWEATHER_API_KEY = import.meta.env.VITE_OPENWEATHER_API_KEY;
const OPENWEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather';
const FALLBACK_URL = 'https://wttr.in';

export async function fetchFromOpenWeather(
  cityName: string
): Promise<WeatherInfo> {
  const res = await fetch(
    `${OPENWEATHER_URL}?q=${encodeURIComponent(
      cityName
    )}&appid=${OPENWEATHER_API_KEY}&units=metric`
  );
  if (!res.ok) throw new Error('City not found');
  const data = await res.json();
  return {
    city: data.name,
    temperature: Math.round(data.main.temp),
    description: data.weather[0].description,
    icon: mapWeatherToIcon(data.weather[0].main),
  };
}

export async function fetchFromFallback(
  cityName: string
): Promise<WeatherInfo> {
  const res = await fetch(
    `${FALLBACK_URL}/${encodeURIComponent(cityName)}?format=j1`
  );
  if (!res.ok) throw new Error('City not found');
  const data = await res.json();
  return {
    city: cityName,
    temperature: Math.round(Number(data.current_condition[0].temp_C)),
    description: data.current_condition[0].weatherDesc[0].value,
    icon: mapWeatherToIcon(data.current_condition[0].weatherDesc[0].value),
  };
}

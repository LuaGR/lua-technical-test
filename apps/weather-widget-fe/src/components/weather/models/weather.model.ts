export interface WeatherInfo {
  city: string;
  temperature: number;
  description: string;
  icon: string;
}

export interface WeatherForm {
  city: string;
  loading: boolean;
  error: string | null;
  lastSearch?: string;
}

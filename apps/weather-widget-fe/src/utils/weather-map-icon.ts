export function mapWeatherToIcon(desc: string): string {
  const d = desc.toLowerCase();
  if (d.includes('rain') || d.includes('lluvia')) return 'rain';
  if (d.includes('cloud') || d.includes('nube')) return 'cloud';
  if (d.includes('sun') || d.includes('sol')) return 'sun';
  if (d.includes('clear') || d.includes('despejado')) return 'sun';
  return 'cloud';
}

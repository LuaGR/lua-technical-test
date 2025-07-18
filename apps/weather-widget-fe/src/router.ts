import { createRouter, createWebHistory } from 'vue-router';
import Weather from './components/weather/weather.vue';

const routes = [
  {
    path: '/weather',
    name: 'Weather',
    component: Weather,
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/weather',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

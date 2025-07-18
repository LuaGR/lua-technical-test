<template>
  <form class="weather-form" @submit.prevent="onSubmit">
    <Input
      id="city"
      v-model="cityModel"
      label="City"
      placeholder="Example: New York, Tokyo"
      :required="true"
      :disabled="loading"
      :error="showCityError || error || undefined"
      autocomplete="off"
      @keyup.enter="onSubmit"
      @blur="cityTouched = true"
    />
    <div class="weather-form__button-wrapper">
      <Button
        type="submit"
        :loading="loading"
        :disabled="!city || loading || !!cityValidationError || isSameSearch"
        class="weather-form__button"
      >
        Search
      </Button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { Input, Button } from '../../../shared';

const props = defineProps<WeatherForm>();

const emit = defineEmits<{
  (e: 'update:city', value: string): void;
  (e: 'submit'): void;
}>();

import { ref } from 'vue';
import { WeatherForm } from '../../models/weather.model';
const cityTouched = ref(false);

const cityModel = computed({
  get: () => props.city,
  set: (value: string) => {
    emit('update:city', value);
    cityTouched.value = true;
  },
});

const cityValidationError = computed(() => {
  if (!cityModel.value) return 'City is required';
  if (/\d/.test(cityModel.value)) return 'City name cannot contain numbers';
  return '';
});

const showCityError = computed(
  () => cityTouched.value && cityValidationError.value
);

const isSameSearch = computed(() => {
  return (
    typeof props.lastSearch === 'string' &&
    props.lastSearch.trim().toLowerCase() ===
      cityModel.value.trim().toLowerCase()
  );
});

function onSubmit() {
  cityTouched.value = true;
  if (cityValidationError.value || isSameSearch.value) return;
  emit('submit');
}
</script>

<style scoped>
.weather-form__button-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 1.5em;
}
</style>

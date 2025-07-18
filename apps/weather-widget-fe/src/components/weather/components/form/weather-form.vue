<template>
  <form class="weather-form" @submit.prevent="onSubmit">
    <Input
      id="city"
      v-model="cityModel"
      label="City"
      placeholder="Example: New York, Tokyo"
      :required="true"
      :disabled="loading"
      :error="error || undefined"
      autocomplete="off"
      @keyup.enter="onSubmit"
    />
    <div class="weather-form__button-wrapper">
      <Button
        type="submit"
        :loading="loading"
        :disabled="!city || loading"
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

const props = defineProps<{
  city: string;
  loading: boolean;
  error: string | null;
}>();

const emit = defineEmits<{
  (e: 'update:city', value: string): void;
  (e: 'submit'): void;
}>();

const cityModel = computed({
  get: () => props.city,
  set: (value: string) => emit('update:city', value),
});

function onSubmit() {
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

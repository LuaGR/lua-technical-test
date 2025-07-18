<script setup lang="ts">
import { computed } from 'vue';
import { Input, Button } from '../../shared';

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

<template>
  <form class="weather-form" @submit.prevent="onSubmit">
    <Input
      id="city"
      v-model="cityModel"
      label="Ciudad"
      placeholder="Ingresa una ciudad"
      :required="true"
      :disabled="loading"
      :error="error"
      autocomplete="off"
      @keyup.enter="onSubmit"
    />
    <Button
      type="submit"
      :loading="loading"
      :disabled="!city || loading"
      class="weather-form__button"
    >
      Buscar
    </Button>
  </form>
</template>

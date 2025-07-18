<template>
  <div class="input-group">
    <Label v-if="label" :for-id="id" :required="required">
      {{ label }}
    </Label>
    <input
      :id="id"
      :type="type"
      :placeholder="placeholder"
      :value="modelValue"
      :disabled="disabled"
      :autocomplete="autocomplete"
      :class="['input', { 'input--error': error }]"
      @input="onInput"
      @blur="onBlur"
      @focus="onFocus"
    />
    <ErrorMessage v-if="error" :message="error" />
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
import { Label, ErrorMessage } from './components';

defineProps({
  id: {
    type: String,
    required: true,
  },
  label: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'text',
  },
  placeholder: {
    type: String,
    default: '',
  },
  modelValue: {
    type: [String, Number],
    default: '',
  },
  required: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  autocomplete: {
    type: String,
    default: 'off',
  },
  error: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['update:modelValue', 'blur', 'focus']);

function onInput(event: Event) {
  const target = event.target as HTMLInputElement;
  emit('update:modelValue', target.value);
}
function onBlur(event: FocusEvent) {
  emit('blur', event);
}
function onFocus(event: FocusEvent) {
  emit('focus', event);
}
</script>

<style scoped>
.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.25em;
}
.input {
  padding: 0.5em 1em;
  border: 1px solid #bdbdbd;
  border-radius: 4px;
  font-size: 1em;
  transition: border 0.2s;
}
.input:focus {
  border-color: #1976d2;
  outline: none;
}
.input--error {
  border-color: #d32f2f;
}
</style>

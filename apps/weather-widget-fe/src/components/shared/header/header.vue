<template>
  <header class="app-header">
    <slot />
  </header>
</template>

<script setup lang="ts"></script>

<style scoped>
.app-header {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2em 0 1.5em 0;
}

.app-header ::v-deep h1 {
  font-size: 2em;
  font-weight: 700;
  color: #1976d2;
  margin: 0;
  letter-spacing: 1px;
}
</style>

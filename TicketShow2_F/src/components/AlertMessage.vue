<template>
  <div :class="`alert alert-${messageType}`" role="alert">
    {{ message }}
  </div>
</template>

<script setup>
const props = defineProps({
  message: {
    type: String,
    required: true,
  },
  messageType: {
    type: String,
    required: true,
  },
});
</script>
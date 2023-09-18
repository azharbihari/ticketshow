<template>
    <div class="d-flex justify-content-center">
        <div class="spinner-grow text" style="width: 3rem; height: 3rem; margin: 320px;" role="status" v-if="isLoading">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
</template>

<script>
import { defineProps } from 'vue';

export default {
    props: {
        isLoading: {
            type: Boolean,
            required: true,
        },
    },
};
</script>

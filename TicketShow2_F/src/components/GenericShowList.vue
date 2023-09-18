<template>
    <div class="row row-cols-2 row-cols-sm-5 g-2">
        <div v-for="show in shows" :key="show.id">
            <router-link class="text-decoration-none" aria-current="page" :to="`/show/${show.id}`">
                <div class="col">
                    <div class="card text-bg-dark h-100">
                        <img :src="show.poster" class="card-img-top" :alt="show.name">
                        <div class="card-body">
                            <p class="lead fw-bold mb-0 text-truncate">{{ show.name }}</p>
                            <small>{{ moment(show.showtime).format('LLLL') }}</small>
                            <small class="">{{ show.genre }} • {{ show.language }}</small>
                        </div>
                    </div>
                </div>
            </router-link>
        </div>
    </div>
</template>

<script setup>
import moment from 'moment';
import { RouterLink } from 'vue-router';

const props = defineProps({
    shows: {
        type: Array,
        required: true,
    },
});
</script>

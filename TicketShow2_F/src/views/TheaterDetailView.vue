<template>
    <main>
        <PageSpinner :isLoading="isLoadingPage" v-if="isLoadingPage"/>
        <div class="container my-5" v-else>
            <h4 class="display-6 text-success mb-4">Upcoming and Running Shows at {{ theater.name }}</h4>
            <GenericShowList :shows="theaterShows" />
        </div>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import GenericShowList from '@/components/GenericShowList.vue';
import api from '@/api';

const props = defineProps({
    theaterId: {
        type: String,
        required: true,
    }
});

const theaterShows = ref([]);
const theater = ref({});
const isLoadingPage = ref(true);

onMounted(async () => {
    fetchTheaterShows();
    isLoadingPage.value = false;
});

async function fetchTheaterShows() {
    try {
        const response = await api.get(`/theaters/${props.theaterId}/shows`);
        theater.value = response.data.theater;
        theaterShows.value = response.data.shows;
    } catch (error) {
        console.error('Failed to fetch theater and shows', error);
    }
}
</script>

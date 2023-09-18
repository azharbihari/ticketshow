<template>
    <main>
        <PageSpinner :isLoading="isLoadingPage" v-if="isLoadingPage"/>
        <div class="container py-5" style="background: linear-gradient(to right, #fdfbfb 0%, #e2ebf0 100%);">
            <SearchShowTheater/>
        </div>
        <div class="container my-5" v-if="userCityShows.length > 0">
            <h4 class="display-6 text-success mb-4">Now Showing in Your City</h4>
            <GenericShowList :shows="userCityShows"/>
            
        </div>

        <div class="container mb-5">
            <h4 class="display-6 mb-4"> Top picks for you </h4>
            <GenericShowList :shows="shows"/>
        </div>
    </main>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { ref, onMounted } from 'vue';
import GenericShowList from '@/components/GenericShowList.vue';
import SearchShowTheater from '@/components/SearchShowTheater.vue';
import api from '@/api';

const { isAuthenticated } = useAuthStore();
const userCityShows = ref([]);
const shows = ref([]);
const isLoadingPage = ref(true);

onMounted(async () => {
    fetchShows();
    if (isAuthenticated) {
        fetchUserCityShows();
    }
    isLoadingPage.value = false;
});

async function fetchShows() {
    try {
        const response = await api.get('/');
        shows.value = response.data;
    } catch (error) {
        console.error('Failed to fetch shows', error);
    }
}

async function fetchUserCityShows() {
    try {
        const response = await api.get('/city/shows');
        userCityShows.value = response.data;
    } catch (error) {
        console.error('Failed to fetch shows', error);
    }
}
</script>
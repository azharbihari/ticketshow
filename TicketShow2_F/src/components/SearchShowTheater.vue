<template>
    <div class="row justify-content-center">
        <div class="col-10 col-sm-6 mb-3">
            <input @keyup="performSearch" v-model="searchTerm" type="search"
                class="form-control rounded-pill border border-secondary"
                placeholder="Search for movies, actors, genres...">
        </div>
    </div>

    <div class="row justify-content-center" v-if="(filteredShows.length > 0 || filteredTheaters.length > 0) && searchTerm">
        <div class="col-10 col-sm-3 mb-3">
            <h4 class="lead ps-2">Shows</h4>
            <div class="list-group" v-if="filteredShows.length > 0">
                <RouterLink class="list-group-item list-group-item-action" :to="`/show/${show.id}`" v-for="show in filteredShows" :key="show.id">
                    <div class="d-flex align-items-center">
                        <img :src="show.poster" alt="Show Poster" class="me-3" style="max-width: 40px; max-height: 60px;">
                        <div>
                            <h6 class="mb-1">{{ show.name }}</h6>
                            <small>{{ show.genre }} • {{ show.language }}</small>
                        </div>
                    </div>
                </RouterLink>
            </div>
            <p class="lead ps-2" v-else>
                No shows found.
            </p>
        </div>

        <div class="col-10 col-sm-3 mb-3">
            <h4 class="lead ps-2">Theaters</h4>
            <div class="list-group" v-if="filteredTheaters.length > 0">
                <RouterLink class="list-group-item list-group-item-action" :to="`/theater/${theater.id}/shows`" v-for="theater in filteredTheaters" :key="theater.id" aria-current="true">
                    <div class="d-flex align-items-center">
                        <i class="bi bi-buildings-fill me-3"></i>
                        <div>
                            <h6 class="mb-1">{{ theater.name }}</h6>
                            <small>{{ theater.city }}</small>
                        </div>
                    </div>
                </RouterLink>
            </div>
            <p class="lead ps-2" v-else>
                No theaters found.
            </p>
        </div>
    </div>

    <p class="lead text-center pb-5" v-if="(filteredShows.length === 0 && filteredTheaters.length === 0) && searchTerm">
        No shows and theaters found. Looks like a scene change!
    </p>
</template>



<script>
import { RouterLink } from 'vue-router';
import { ref } from 'vue';
import api from '@/api';

export default {
    setup() {
        const searchTerm = ref('');
        const filteredShows = ref([]);
        const filteredTheaters = ref([]);

        const performSearch = async () => {
            try {
                await filterShows(searchTerm.value);
            } catch (error) {
                console.error('Failed to filter shows', error);
            }
        };

        async function filterShows(searchTerm) {
            try {
                const response = await api.get('/search', { params: { searchTerm } });
                filteredTheaters.value = response.data.theaters;
                filteredShows.value = response.data.shows;
            } catch (error) {
                console.error('Failed to fetch shows', error);
            }
        }

        return {
            searchTerm,
            filteredShows,
            filteredTheaters,
            performSearch,
            RouterLink,
        };
    },
};
</script>

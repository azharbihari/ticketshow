<template>
    <main>
        <PageSpinner :isLoading="isLoadingPage" v-if="isLoadingPage" />
        <div class="container my-5" v-else>
            <p class="display-5"> Insights </p>

            <div class="row row-cols-1 row-cols-sm-2 align-items-stretch g-2">
                <div class="col">
                    <div class="card shadow rounded">
                        <div class="card-body">
                            <p class="lead fs-4 mb-0">Top Five Shows by Revenue</p>
                            <img :src="insights.top_five_shows_by_revenue" class="img-fluid" alt="">
                        </div>
                    </div>
                </div>

                <div class="col">
                    <div class="card shadow rounded">
                        <div class="card-body">
                            <p class="lead fs-4 mb-0">User Activity Funnel Analysis</p>
                            <img :src="insights.user_activity_funnel_analysis" class="img-fluid" alt="">
                        </div>
                    </div>
                </div>

            </div>
            <div class="row row-cols-1 row-cols-sm-3 align-items-stretch g-2 mt-2">
                <div class="col">
                    <div class="card bg-success-subtle shadow rounded">
                        <div class="card-body">
                            <p class="lead fs-4 mb-0">Most Visited Show</p>
                            <h1 class="display-6 fw-bold">{{ insights.most_visited_show.name }}</h1>
                        </div>
                    </div>



                    <div class="card bg-light-subtle shadow rounded mt-2">
                        <h1 class="card-header lead">Top 5 Highest Rated Shows</h1>
                        <ol class="list-group list-group-numbered">
                            <li v-for="show in insights.top_5_highest_rated_shows" :key="show.id" class="list-group-item d-flex justify-content-between align-items-start">
                                <div class="ms-2 me-auto">
                                    <div class="fw-bold">{{ show.name }}</div>
                                    {{ show.genre }} • {{ show.language }}
                                </div>
                            </li>
                        </ol>
                    </div>
                    
                    <div class="card bg-info-subtle shadow rounded mt-2">
                        <div class="card-body">
                            <p class="lead fs-4 mb-0">Most Active User</p>
                            <h1 class="display-6 fw-bold">{{ insights.most_active_user.first_name }} {{ insights.most_active_user.last_name }}</h1>
                        </div>
                    </div>
                    <div class="card bg-light-subtle shadow rounded mt-2">
                        <h1 class="card-header lead">Top 5 Most Spending Users</h1>
                        <ol class="list-group list-group-numbered">
                            <li v-for="user in insights.top_5_highest_spending_users" :key="user.id" class="list-group-item d-flex justify-content-between align-items-start">
                                <div class="ms-2 me-auto">
                                    <div class="fw-bold">{{ user.first_name }} {{ user.last_name }}</div>
                                    {{ user.city }}
                                </div>
                            </li>
                        </ol>
                    </div>
                </div>


                <div class="col">
                    <div class="card bg-light-subtle shadow rounded">
                        <h1 class="card-header lead">Top 5 Most Visited Shows</h1>
                        <ol class="list-group list-group-numbered">
                            <li v-for="show in insights.top_5_most_visited_shows" :key="show.id" class="list-group-item d-flex justify-content-between align-items-start">
                                <div class="ms-2 me-auto">
                                    <div class="fw-bold">{{ show.name }}</div>
                                    {{ show.genre }} • {{ show.language }}
                                </div>
                            </li>
                        </ol>
                    </div>

                    <div class="card bg-dark-subtle shadow rounded mt-2">
                        <div class="card-body">
                            <p class="lead fs-4 mb-0">City with the Most Active Users</p>
                            <h1 class="display-6 fw-bold">{{ insights.city_with_most_active_users.city }}</h1>
                        </div>
                    </div>

                    <div class="card bg-light-subtle shadow rounded mt-2">
                        <h1 class="card-header lead">Top 5 Shows With Unique Visitors</h1>
                        <ol class="list-group list-group-numbered">
                            <li v-for="show in insights.top_5_shows_with_unique_visitors" :key="show.id" class="list-group-item d-flex justify-content-between align-items-start">
                                <div class="ms-2 me-auto">
                                    <div class="fw-bold">{{ show.name }}</div>
                                    {{ show.genre }} • {{ show.language }}
                                </div>
                            </li>
                        </ol>
                    </div>
                </div>

                <div class="col">
                    <div class="card text-bg-primary shadow rounded">
                        <div class="card-body">
                            <p class="lead fs-4 mb-0">Total Number of Bookings</p>
                            <h1 class="display-1 fw-bold">{{ insights.total_number_of.bookings }}</h1>
                        </div>
                    </div>

                    <div class="card text-bg-success shadow rounded mt-2">
                        <div class="card-body">
                            <p class="lead fs-4 mb-0">Total Number of Shows</p>
                            <h1 class="display-1 fw-bold">{{ insights.total_number_of.shows }}</h1>
                        </div>
                    </div>

                    <div class="card text-bg-dark shadow rounded mt-2">
                        <div class="card-body">
                            <p class="lead fs-4 mb-0">Total Number of Theaters</p>
                            <h1 class="display-1 fw-bold">{{ insights.total_number_of.theaters }}</h1>
                        </div>
                    </div>


                    <div class="card text-bg-info shadow rounded mt-2">
                        <div class="card-body">
                            <p class="lead fs-4 mb-0">Total Number of Users</p>
                            <h1 class="display-1 fw-bold">{{ insights.total_number_of.users }}</h1>
                        </div>
                    </div>

                    <div class="card text-bg-warning shadow rounded mt-2">
                        <div class="card-body">
                            <p class="lead fs-4 mb-0">Total Number of Reviews</p>
                            <h1 class="display-1 fw-bold">{{ insights.total_number_of.reviews }}</h1>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </main>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';

const insights = ref([]);
const isLoadingPage = ref(true);

onMounted(async () => {
    await fetchInsights();
});

async function fetchInsights() {
    try {
        const response = await api.get('/insights');
        insights.value = response.data;
        isLoadingPage.value = false;
    } catch (error) {
        console.error('Failed to fetch insights', error);
    }
}
</script>
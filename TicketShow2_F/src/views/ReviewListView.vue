<template>
    <main>
        <PageSpinner :isLoading="isLoadingPage" v-if="isLoadingPage" />
        <div class="container my-5" v-else>
                        <router-link class="btn btn-secondary btn-sm float-end" aria-current="page"
                        :to="`/${show.theater.id}/shows`"><i class="bi bi-arrow-left"></i> Shows</router-link>
            <div class="">
                <h3 class="mb-0"><small class="text-body-secondary">Reviews for show</small> {{ show.name }}</h3>
                <p class=""><span class="text-body-secondary">Date & time: </span> {{ moment(show.showtime).format('LLLL')
                }} </p>
            </div>
            <hr>

            <div class="table-responsive">
                <table class="table table-sm table-hover">
                    <thead>
                        <tr>
                            <th>Reviewer</th>
                            <th>Comment</th>
                            <th>Rating</th>
                        </tr>
                    </thead>
                    <tbody v-if="reviews.length > 0">
                        <tr v-for="review in reviews" :key="review.id">
                            <td>
                                <p class="mb-0 fw-bold">{{ review.user.first_name }} {{ review.user.last_name }}</p>
                                <small class="text-secondary"> Reviewed at {{
                                    moment(review.created_at).startOf('second').fromNow() }}</small>
                            </td>
                            <td>{{ review.comment }}</td>
                            <td>{{ review.rating }}</td>
                        </tr>
                    </tbody>

                    <tbody v-else>
                        <tr>
                            <td colspan="3">No reviews available.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import moment from 'moment';
const isLoadingPage = ref(true);
const reviews = ref([]);
const show = ref({});

const props = defineProps({
    showId: {
        type: String,
        required: true,
    },
});

onMounted(async () => {
    await fetchReviews();
});

async function fetchReviews() {
    try {
        const response = await api.get(`/${props.showId}/reviews`);
        reviews.value = response.data.reviews;
        show.value = response.data.show;
        isLoadingPage.value = false;
    } catch (error) {
        console.error('Failed to fetch reviews', error);
    }
}
</script>

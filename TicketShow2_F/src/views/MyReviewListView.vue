<template>
    <main>
        <PageSpinner :isLoading="isLoadingPage" v-if="isLoadingPage" />
        <div class="container my-5" v-else>
            <MyAccountNav />
            <div v-if="mybookings.length > 0" class="row row-cols-1 row-cols-md-3 g-2 justify-content-sm-center mt-5"
                data-masonry='{"percentPosition": true }'>
                <div class="col" v-for="booking in mybookings" :key="booking.id">
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title mb-0 text-truncate">{{ booking.show.name }}</h5>
                            <p class="card-text text-body-secondary" style="font-size: 12px;">Booked at {{
                                moment(booking.created_at).startOf('second').fromNow() }}</p>
                            <div class="" v-if="booking.review">
                                <p>Rating <span class="badge text-bg-secondary">{{ booking.review.rating }}</span></p>
                                <p class="text-primary"> {{ booking.review.comment }}</p>
                                <div class="hstack gap-2">
                                    <button @click="deleteReview(booking)" class="btn btn-danger btn-sm"> Delete Review
                                    </button>
                                </div>
                            </div>

                            <div v-else>
                                <p class="text-primary small">
                                    We hope you enjoyed the show you booked and watched recently. Please take a moment to
                                    write a review and share your experience.
                                </p>

                                <button @click="selectedBooking = booking" type="button" class="btn btn-primary btn-sm"
                                    data-bs-toggle="modal" data-bs-target="#staticBackdrop">
                                    Write a Review
                                </button>
                            </div>
                        </div>
                    </div>
                </div>


                <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
                    aria-labelledby="staticBackdropLabel" aria-hidden="true">
                    <div class="modal-dialog model-sm">
                        <div class="modal-content">

                            <div class="modal-body text-center" v-if="showThankYou">
                                <i class="bi bi-check-circle-fill text-success fs-1 mb-3"></i>
                                <h5 class="mb-3">Thank you for your review!</h5>
                                <p class="text-center">
                                    Your valuable feedback helps us improve our services and create a better movie
                                    experience for you. We appreciate your support and hope to see you again soon!
                                </p>
                                <button @click="showThankYou = false" type="button" class="btn btn-primary"
                                    data-bs-dismiss="modal">Close</button>
                            </div>

                            <div class="modal-body" v-else>
                                <h5 class="mb-3">Write a Review</h5>
                                <form @submit.prevent="addReview()">
                                    <div class="mb-3">
                                        <select class="form-select" v-model="review.rating">
                                            <option disabled>Select a Rating</option>
                                            <option value="1">Terrible</option>
                                            <option value="2">Poor</option>
                                            <option value="3">Average</option>
                                            <option value="4">Good</option>
                                            <option value="5">Excellent</option>
                                        </select>
                                    </div>

                                    <div class="mb-3">
                                        <textarea class="form-control" id="comment" required rows="3"
                                            v-model="review.comment" placeholder="Enter your review..."></textarea>
                                    </div>

                                    <div class="">
                                        <button type="button" class="btn btn-secondary me-2" @click="clearForm"
                                            data-bs-dismiss="modal">Close</button>
                                        <button type="submit" class="btn btn-primary">Submit</button>
                                    </div>
                                </form>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
            <p v-else class="text-center mt-5"> No bookings found for review. Book your first ticket.</p>
        </div>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import moment from 'moment';
import MyAccountNav from '@/components/MyAccountNav.vue';

const mybookings = ref([]);
const selectedBooking = ref(null);
const review = ref({ rating: 3, comment: '' });
const showThankYou = ref(false);
const isLoadingPage = ref(true);

onMounted(async () => {
    await fetchMyBookings();
});

async function fetchMyBookings() {
    try {
        const response = await api.get('/myreviews');
        mybookings.value = response.data;
        isLoadingPage.value = false;
    } catch (error) {
        console.error('Failed to fetch bookings', error);
    } finally {
        isLoadingPage.value = false;
    }
}

async function deleteReview(booking) {
    try {
        const confirmed = confirm('Are you sure you want to delete this review?');
        if (confirmed) {
            const response = await api.delete(`/${booking.id}/myreviews`);
            if (response.status === 200) {
                fetchMyBookings();
                console.log('Review deleted');
            } else {
                console.error('Failed to delete review');
            }
        }
    } catch (error) {
        console.error('Failed to delete review', error);
    }
}

async function addReview() {
    const booking = selectedBooking.value;
    if (booking) {
        try {
            const response = await api.post(`${booking.id}/myreviews`, review.value);
            if (response.status === 201) {
                fetchMyBookings();
                console.log('Review added');
                clearForm();
                showThankYou.value = true;
            } else {
                console.error('Failed to add review');
            }
        } catch (error) {
            console.error('Failed to add review', error);
        }
    }
}

function clearForm() {
    selectedBooking.value = null;
    review.value = { rating: 2, comment: '' };
}
</script>

<template>
    <main>
        <PageSpinner :isLoading="isLoadingPage" v-if="isLoadingPage"/>
        <div class="container my-5" v-else>
            <router-link class="btn btn-secondary btn-sm float-end" aria-current="page"
                    :to="`/${show.theater.id}/shows`"><i class="bi bi-arrow-left"></i> Shows</router-link>
            <div class="">
                <h3 class="mb-0"><small class="text-body-secondary">Bookings for show</small> {{ show.name }}</h3>
                <p class=""><span class="text-body-secondary">Date & time: </span> {{ moment(show.showtime).format('LLLL') }} </p>
            </div>
            <hr>


            <div class="row mb-3">
                <label for="selectedStatus" class="col-auto col-form-label">Filter by Status: </label>
                <div class="col-auto">
                    <select class="form-control" v-model="selectedStatus" id="selectedStatus">
                        <option value="All">All</option>
                        <option value="Confirmed">Confirmed</option>
                        <option value="Cancelled">Cancelled</option>
                    </select>
                </div>
            </div>
            <hr>

            <div class="table-responsive">        
                <table class="table table-sm table-hover">
                    <thead>
                        <tr>
                            <th>Booking Details</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody v-if="filteredBookings.length > 0">
                        <tr v-for="booking in filteredBookings" :key="booking.id">
                            <td>
                                <p class="lead fw-bold mb-0">{{ booking.user.first_name }} {{ booking.user.last_name }}</p>
                                <div class="hstack gap-3">
                                    <p class="text-secondary small">Booked at {{ moment(booking.created_at).format('LLLL') }}</p>
                                    <p class=""><i class="bi bi-ticket-detailed-fill"></i> {{ booking.number_of_tickets }}</p>
                                    <p class=""><i class="bi bi-cash"></i> ₹{{ booking.amount }}</p>
                                </div>

                            </td>
                            <td>
                                <span class="badge rounded-pill text-bg-success" v-if="booking.status === 'Confirmed'">Confirmed</span>
                                <span class="badge rounded-pill text-bg-danger" v-else >Cancelled</span>
                            </td>
                        </tr>
                    </tbody>

                    <tbody v-else>
                        <tr> <td colspan="2">No bookings available.</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
</template>

<script setup>
import { ref, onMounted, computed, defineProps } from 'vue';
import api from '@/api';
import moment from 'moment';

const isLoadingPage = ref(true);
const bookings = ref([]);
const show = ref({});

const props = defineProps({
    showId: {
        type: String,
        required: true,
    },
});

const selectedStatus = ref('All');

onMounted(async () => {
    await fetchBookings();
});

async function fetchBookings() {
    try {
        const response = await api.get(`/${props.showId}/bookings`);
        bookings.value = response.data.bookings;
        show.value = response.data.show;
        isLoadingPage.value = false;
    } catch (error) {
        console.error('Failed to fetch bookings', error);
    }
}

const filteredBookings = computed(() => {
    if (selectedStatus.value === 'All') {
        return bookings.value;
    } else {
        return bookings.value.filter(booking => booking.status === selectedStatus.value);
    }
});
</script>
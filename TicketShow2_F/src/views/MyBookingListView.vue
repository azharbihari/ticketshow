<template>
    <main>
        <PageSpinner :isLoading="isLoadingPage" v-if="isLoadingPage" />
        <div class="container my-5" v-else>
            <MyAccountNav />
            <div v-if="mybookings.length > 0" class="row row-cols-1 row-cols-md-3 g-2 justify-content-sm-center mt-5">
                <div class="col" v-for="booking in mybookings" :key="booking.id">
                    <div class="card mb-3">
                        <div class="row g-0">
                            <div class="col-md-3 d-flex">
                                <img :src="booking.show.poster" class="img-fluid rounded" :alt="booking.show.name">
                            </div>
                            <div class="col-md-9">
                                <div class="card-body">
                                    <h5 class="card-title mb-1 text-truncate">{{ booking.show.name }}</h5>
                                    <p class="card-text mb-1">{{ booking.show.genre }} • {{ booking.show.language }}</p>
                                    <p class="card-text mb-1"><i class="bi bi-ticket-detailed-fill"></i> {{
                                        booking.number_of_tickets }} • <i class="bi bi-cash"></i> ₹{{ booking.amount }}</p>
                                    <p class="card-text mb-1"><small class="text-body-secondary"><i
                                                class="bi bi-alarm-fill"></i> {{
                                                    moment(booking.show.showtime).format('LLLL') }}</small></p>
                                    <div class="">
                                        <button
                                            v-if="['Pending', 'Confirmed'].includes(booking.status) && booking.show.status === 'Upcoming'"
                                            @click="deleteBooking(booking)" class="btn btn-danger btn-sm">Cancel
                                            Booking</button>
                                        <p v-if="booking.status === 'Cancelled'" class="text-danger"> Booking Cancelled</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <p v-else class="text-center mt-5"> No bookings found. Book your first ticket.</p>
        </div>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import moment from 'moment';
import MyAccountNav from '@/components/MyAccountNav.vue';

const mybookings = ref([]);
const isLoadingPage = ref(true);

onMounted(async () => {
    await fetchMyBookings();
});

async function fetchMyBookings() {
    try {
        const response = await api.get('/mybookings');
        mybookings.value = response.data;
        isLoadingPage.value = false;
    } catch (error) {
        console.error('Failed to fetch bookings', error);
    } finally {
        isLoadingPage.value = false;
    }
}

async function deleteBooking(booking) {
    try {
        const confirmed = confirm('Are you sure you want to cancel this booking?');
        if (confirmed) {
            const response = await api.delete(`/mybookings/${booking.id}`);
            if (response.status === 200) {
                fetchMyBookings();
            } else {
                console.error('Failed to delete booking');
            }
        }
    } catch (error) {
        console.error('Failed to cancel booking', error);
    }
}
</script>

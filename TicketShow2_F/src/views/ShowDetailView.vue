<template>
    <main>
        <PageSpinner :isLoading="isLoadingPage" v-if="isLoadingPage"/>
        <div class="container my-5">
            <div v-if="show && !isbooked" class="card border-0">
                <div class="row g-3">
                    <div class="col-sm-3 d-flex">
                        <img :src="show.poster" class="img-fluid rounded-start mb-auto flex-fill" alt="...">
                    </div>
                    
                    <div class="col-sm-9">
                        <div class="card-body">
                            <h1 class="card-title display-4">{{ show.name }}</h1>                            
                            <p class="lead fw-normal text-primary">
                                <span>{{ show.runtime }} minutes</span> • <span>{{ show.genre }}</span> • <span>{{ show.language }}</span>
                            </p>

                            <p class="lead fw-bolder">{{ moment(show.showtime).format('LLLL') }}</p>  
                            
                            

                            <div v-if="show.is_housefull">
                                <p class="text-info fw-bold display-4">Housefull</p>
                                <p class="fw-bold">We're sorry, all tickets for this show have been sold out.<br>
                                        Thank you for your interest and we hope to see you at our future shows.</p>
                            </div>

                            <div class="" v-else>
                                <form @submit.prevent="addBooking" v-if="isBooking" class="row g-2">
                                    
                                    <div class="col-sm-2">
                                        <input aria-describedby="numberOfTickets" type="number" :min="1" :max="show.available_tickets" class="form-control" v-model="booking.number_of_tickets" required>
                                        <div id="numberOfTickets" class="form-text" v-if="booking.number_of_tickets >= show.available_tickets">{{ show.available_tickets }} tickets available</div>
                                    </div>

                                    <div class="col-auto">
                                        <p class="lead form-control px-3">₹{{ calculateAmount }}</p>
                                    </div>

                                    <div class="col-12">
                                        <button type="submit" class="btn btn-danger btn-lg">{{ isLoading ? 'Loading...' : 'Confirm to Book' }}</button>
                                    </div>
                                </form>
                                <button v-else @click="isBooking=true" class="btn btn-danger btn-lg" >Book Tickets</button>
                            </div>


                            <div class="row mt-5">
                                <h6 class="lead fw-bold mb-1">Description</h6>
                                <p class="card-text">{{ show.description }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div v-else class="card border-0">
                <div class="card-body text-center" v-if="isbooked" style="margin: 120px 0px;">
                    <h3 class="display-1 fw-bold">🎉</h3>
                    <h3 class="display-5 fw-bold">Congratulations!</h3>
                    <p class="display-6">Your booking is confirmed.</p>
                    <div class="hstack gap-2 justify-content-center">
                        <RouterLink class="btn btn-danger" to="/">Explore Shows</RouterLink>
                        <RouterLink class="btn btn-success" to="/mybookings">My Bookings</RouterLink>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import moment from 'moment';
import api from '@/api';
import JSConfetti from 'js-confetti';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const confetti = new JSConfetti();

const props = defineProps({
    showId: {
        type: String,
        required: true,
    },
});

const show = ref({});
const isLoadingPage = ref(true);
const isbooked = ref(false);
const booking = ref({ number_of_tickets: 1 });
const isLoading = ref(false);
const isBooking = ref(false);
const authStore = useAuthStore();
const router = useRouter();

onMounted(async () => {
    fetchShow();
    isLoadingPage.value = false;
});

async function fetchShow() {
    try {
        const response = await api.get(`/${props.showId}`);
        show.value = response.data;
    } catch (error) {
        console.error('Failed to fetch show', error);
    }
}

const calculateAmount = computed(() => {
    const numberOfTickets = booking.value.number_of_tickets;
    const ticketPrice = show.value.ticket_price;

    if (typeof numberOfTickets === 'number' && typeof ticketPrice === 'number') {
        return numberOfTickets * ticketPrice;
    }

    return 0;
});

async function addBooking() {
    const isAuthenticated = authStore.isAuthenticated;
    if (isAuthenticated) {
        try {
            const response = await api.post(`${props.showId}/mybookings`, booking.value);
            if (response.status === 201) {
                isbooked.value = true;
                fetchShow();
                confetti.addConfetti();
            } else {
                console.error('Failed to add booking');
            }
        } catch (error) {
            console.error('Failed to add booking', error);
        }
    } else {
        router.push('/login');
    }
}
</script>
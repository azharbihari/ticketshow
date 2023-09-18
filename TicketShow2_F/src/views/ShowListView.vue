<template>
    <main>
        <PageSpinner :isLoading="isLoadingPage" v-if="isLoadingPage"/>
        <div class="container my-5" v-else>
            <RouterLink class="btn float-end btn-sm btn-secondary" aria-current="page" to="/dashboard"><i class="bi bi-arrow-left"></i> Dashboard</RouterLink>
            <div class="">
                <h3 class="mb-0"><small class="text-body-secondary">Shows for theater</small> {{ theater.name }}</h3>
                <p class=""><span class="text-body-secondary">City: </span>{{ theater.city }}, <span class="text-body-secondary">Capacity: </span>{{ theater.capacity }}</p>
            </div>
            <hr>
            <AlertMessage v-if="isMessage" :message="message" :messageType="messageType"/>


            <div class="row ">
                <div class="col-sm-8">
                    <ShowList :editMode="editMode" :show="show" @fetchShows="fetchShows" :theaterId="theaterId" :shows="shows" @deleteShow="deleteShow"
                        @editShow="editShow"/>
                </div>
                <div class="col-sm-4">
                    <AddShow :editMode="editMode" :show="show" @updateShow="updateShow" @addShow="addShow" />
                </div>
            </div>
        </div>
    </main>
</template>

<script setup>
import AddShow from '@/components/AddShow.vue';
import ShowList from '@/components/ShowList.vue';
import { ref, onMounted } from 'vue';
import api from '@/api';

const shows = ref([]);
const show = ref({});
const theater = ref({});
const editMode = ref(false);
const isLoadingPage = ref(true);
const message = ref('');
const messageType = ref('');
const isMessage = ref(false);

const props = defineProps({
    theaterId: {
        type: String,
        required: true,
    },
});

onMounted(async () => {
    await fetchShows();
});

function handleResponse(messageText, type) {
    message.value = messageText;
    messageType.value = type;
    isMessage.value = true;
    setTimeout(() => {
        isMessage.value = false;
        message.value = '';
        messageType.value = '';
    }, 3000);
}

async function fetchShows() {
    try {
        const response = await api.get(`/${props.theaterId}/shows`);
        shows.value = response.data.shows;
        theater.value = response.data.theater;
        isLoadingPage.value = false;
    } catch (error) {
        console.error('Failed to fetch shows', error);
    }
}

async function deleteShow(show) {
    try {
        const confirmed = confirm(`Are you sure you want to delete the show ${show.name}?`);
        if (confirmed) {
            const response = await api.delete(`/shows/${show.id}`);
            if (response.status === 200) {
                fetchShows();
                handleResponse(response.data.message, 'success');
            } else {
                console.error('Failed to delete show');
            }
        }
    } catch (error) {
        console.error('Failed to delete show', error);
    }
}

function editShow(selectedShow) {
    editMode.value = true;
    show.value = { ...selectedShow };
}

async function updateShow(show) {
    try {
        const response = await api.put(`/shows/${show.id}`, show);

        if (response.status === 200) {
            fetchShows();
            resetForm();
            handleResponse(response.data.message, 'success');
        } else {
            console.error('Failed to update show');
        }
    } catch (error) {
        handleResponse(error.response.data.message, 'danger');
        console.error('Failed to update show', error);
    }
}

async function addShow(show) {
    try {
        const response = await api.post(`/${props.theaterId}/shows`, show);
        if (response.status === 201) {
            fetchShows();
            resetForm();
            handleResponse(response.data.message, 'success');
        } else {
            console.error('Failed to add show');
        }
    } catch (error) {
        handleResponse(error.response.data.message, 'danger');
        console.error('Failed to add show', error);
    }
}

function resetForm() {
    show.value = {};
}
</script>
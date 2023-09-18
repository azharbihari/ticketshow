<template>
<main>
    <PageSpinner :isLoading="isLoadingPage" v-if="isLoadingPage"/>
    <div class="container my-5" v-else>
        <p class="display-5"> Welcome to Dashboard!</p>
        <AlertMessage v-if="isMessage" :message="message" :messageType="messageType"/>

        <div v-if="taskStatus !== ''" class="my-4">
            <p v-if="taskStatus === 'SUCCESS'" class="text-success fw-bold">Export successful!
                <a class="icon-link icon-link-hover" :href="csvUrl" style="--bs-link-hover-color-rgb: 25, 135, 84;">
                    Download CSV <i class="bi bi-box-arrow-down"></i>
                </a>
            </p>
            <p v-else-if="taskStatus === 'FAILURE'" class="text-danger">Export failed.</p>
            
            <div v-else class="d-flex align-items-center">
                <div class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></div><strong class="ms-2">Export in progress. Please wait...</strong>
            </div>
        </div>

        <div class="row">
            <div class="col-sm-8">
                <TheaterList :editMode="editMode" :theater="theater" :theaters="theaters" @exportTheater="exportTheater" @deleteTheater="deleteTheater" @editTheater="editTheater"/>
            </div>
            <div class="col-sm-4">
                <AddTheater :editMode="editMode" :theater="theater" @updateTheater="updateTheater" @addTheater="addTheater"/>
            </div>
        </div>
    </div>
</main>
</template>


<script setup>
import AddTheater from '@/components/AddTheater.vue';
import TheaterList from '@/components/TheaterList.vue';
import { ref, onMounted } from 'vue';
import api from '@/api';

const csvUrl = ref('');
const taskStatus = ref('');
const theaters = ref([]);
const theater = ref({});

const editMode = ref(false);
const isLoadingPage = ref(true);
const message = ref('');
const messageType = ref('');
const isMessage = ref(false);

onMounted(async () => {
    await fetchTheaters();
});

async function fetchTheaters() {
    try {
        const response = await api.get('/theaters');
        theaters.value = response.data;
        isLoadingPage.value = false;
    } catch (error) {
        console.error('Failed to fetch theaters', error);
    }
}

async function deleteTheater(theater) {
    try {
        const confirmed = confirm(`Are you sure you want to delete the theater ${theater.name}?`);
        if (confirmed) {
            const response = await api.delete(`/theaters/${theater.id}`);
            if (response.status === 200) {
                await fetchTheaters();
                handleResponse(response.data.message, 'success');
            } else {
                console.error('Failed to delete theater');
            }
        }
    } catch (error) {
        console.error('Failed to delete theater', error);
    }
}

async function updateTheater(theater) {
    try {
        const response = await api.put(`/theaters/${theater.id}`, theater);
        if (response.status === 200) {
            editMode.value = false;
            await fetchTheaters();
            handleResponse(response.data.message, 'success');
        } else {
            console.error('Failed to update theater');
        }
    } catch (error) {
        console.error('Failed to update theater', error);
    }
}

async function addTheater(theater) {
    try {
        const response = await api.post('/theaters', theater);
        if (response.status === 201) {
            await fetchTheaters();
            resetForm();
            handleResponse(response.data.message, 'success');
        } else {
            console.error('Failed to add theater');
        }
    } catch (error) {
        console.error('Failed to add theater', error);
    }
}

function resetForm() {
    theater.value = {};
}

function editTheater(selectedTheater) {
    editMode.value = true;
    theater.value = selectedTheater;
}

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

async function exportTheater(theater) {
    try {
        const response = await api.get(`/exports/${theater.id}`);
        checkExportStatus(response.data);
    } catch (error) {
        console.error('Failed to fetch shows', error);
    }
}

async function checkExportStatus(taskId) {
    try {
        const interval = setInterval(async () => {
            try {
                const response = await api.get(`/exports/${taskId}/status`);
                taskStatus.value = response.data.status;
                if (taskStatus.value === 'SUCCESS') {
                    csvUrl.value = response.data.csv_url;
                    console.log(csvUrl.value);
                    clearInterval(interval);
                } else if (taskStatus.value === 'FAILURE') {
                    console.error('Export task failed');
                    clearInterval(interval);
                }
            } catch (error) {
                console.error('Failed to check export status', error);
                clearInterval(interval);
            }
        }, 2000);
    } catch (error) {
        console.error('Failed to check export status', error);
    }
}
</script>
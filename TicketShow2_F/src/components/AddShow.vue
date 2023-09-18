<template>
    <div class="bg-light p-3">
        <h3>{{ editMode ? 'Edit Show' : 'New Show' }}</h3>
        <form @submit.prevent="handleFormSubmit">
            <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" class="form-control" id="name" v-model="show.name" required>
            </div>

            <div class="row mb-3 g-2">
                <div class="col-6">
                    <label for="genre" class="form-label">Genre</label>
                    <input type="text" class="form-control" id="genre" v-model="show.genre" required>
                </div>

                <div class="col-6">
                    <label for="language" class="form-label">Language</label>
                    <input type="text" class="form-control" id="language" v-model="show.language" required>
                </div>
            </div>



            <div class="row mb-3 g-2">
                <div class="col-6">
                    <label for="ticket_price" class="form-label">Ticket Price</label>
                    <input type="number" class="form-control" id="ticket_price" v-model.number="show.ticket_price" required>
                </div>
                <div class="col-6">
                    <label for="runtime" class="form-label">Runtime</label>
                    <input type="number" class="form-control" id="runtime" v-model.number="show.runtime" required>
                </div>
            </div>

            <div class="mb-3">
                <label for="datetime" class="form-label">Showtime</label>
                <input type="datetime-local" :min="minDatetime" class="form-control" id="datetime" v-model="show.showtime" required>
            </div>

            <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea class="form-control" id="description" v-model="show.description" required rows="3"></textarea>
            </div>
            <p>{{ error }}</p>
            <button type="submit" class="btn btn-primary">{{ editMode ? 'Update Show' : 'Add Show' }}</button>
        </form>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    show: {
        type: Object,
        required: true,
    },
    editMode: {
        type: Boolean,
        required: true,
    },
});

const minDatetime = computed(() => {
    const currentDateTime = new Date().toISOString().slice(0, 16);
    return currentDateTime;
});

const emits = defineEmits(['updateShow', 'addShow']);

function handleFormSubmit() {
    if (props.editMode) {
        emits('updateShow', props.show);
    } else {
        emits('addShow', props.show);
    }
}
</script>
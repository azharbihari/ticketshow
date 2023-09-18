<template>
    <div class="bg-light p-3">
        <h3>{{ editMode ? 'Edit Theater' : 'New Theater' }}</h3>
        <form @submit.prevent="handleFormSubmit">
            <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" class="form-control" id="name" v-model="theater.name" required>
            </div>

            <div class="row g-2 mb-3">
                <div class="col-8">
                    <label for="city" class="form-label">City</label>
                    <input type="text" class="form-control" id="city" v-model="theater.city" required>
                </div>
                <div class="col-4">
                    <label for="capacity" class="form-label">Capacity</label>
                    <input type="number" class="form-control" id="capacity" v-model.number="theater.capacity" required>
                </div>
            </div>

            <button type="submit" class="btn btn-primary">{{ editMode ? 'Update Theater' : 'Add Theater' }}</button>
        </form>
    </div>
</template>

<script setup>
const props = defineProps({
    theater: {
        type: Object,
        required: true,
    },
    editMode: {
        type: Boolean,
        required: true,
    },
});

const emits = defineEmits(['updateTheater', 'addTheater']);

function handleFormSubmit() {
    if (props.editMode) {
        emits('updateTheater', props.theater);
    } else {
        emits('addTheater', props.theater);
    }
}
</script>
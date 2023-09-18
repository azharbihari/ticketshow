<template>
  <div>
    <div class="table-responsive">
      <table class="table table-sm table-hover">
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>City</th>
            <th>Capacity</th>
            <th></th>
          </tr>
        </thead>
        <tbody v-if="theaters.length > 0">
          <tr v-for="(theater, index) in theaters" :key="theater.id">
            <td>{{ index + 1 }}</td>
            <td>{{ theater.name }}</td>
            <td>{{ theater.city }}</td>
            <td>{{ theater.capacity }}</td>
            <td>
              <router-link class="btn btn-info btn-sm me-1" aria-current="page"
                :to="`/${theater.id}/shows`">Shows</router-link>
              <button @click="editTheater(theater)" :class="{
                'btn btn-warning btn-sm me-1': theater !== selectedTheater,
                'btn btn-outline-warning btn-sm me-1': theater === selectedTheater
              }">Edit</button>
              <button @click="deleteTheater(theater)" class="btn btn-danger btn-sm me-1">Delete</button>
              <button @click="exportTheater(theater)" class="btn btn-secondary btn-sm me-1">Export <i
                  class="bi bi-filetype-csv"></i></button>
            </td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr>
            <td colspan="5">No Theaters available.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps({
  theaters: {
    type: Array,
    required: true
  }
});

const selectedTheater = ref({});
const emits = defineEmits(['deleteTheater', 'editTheater', 'exportTheater']);

function deleteTheater(theater) {
  emits('deleteTheater', theater);
}

function editTheater(theater) {
  emits('editTheater', theater);
  selectedTheater.value = theater;
}

function exportTheater(theater) {
  emits('exportTheater', theater);
}
</script>

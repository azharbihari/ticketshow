<template>
  <div>
    <div class="row mb-3">
      <label for="selectedStatus" class="col-auto col-form-label">Filter by Status:</label>
      <div class="col-auto">
        <select class="form-control" v-model="selectedStatus" id="selectedStatus">
          <option value="All">All</option>
          <option value="Upcoming">Upcoming</option>
          <option value="Finished">Finished</option>
          <option value="Running">Running</option>
        </select>
      </div>
    </div>
    <hr />

    <div class="table-responsive">
      <table class="table table-sm table-hover">
        <thead>
          <tr>
            <th>Poster</th>
            <th>Show Details</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody v-if="filteredShows.length > 0">
          <tr v-for="show in filteredShows" :key="show.id">
            <td>
              <img :src="show.poster" style="cursor: pointer; width: 120px;" class="img-fluid rounded"
                @click="changePoster(show)" alt="poster" data-bs-toggle="tooltip" title="Change Poster" />
            </td>

            <td>
              <p class="lead fw-bold mb-0">{{ show.name }}</p>
              <p class="">
                <span>{{ show.runtime }} minutes</span> • <span>{{ show.genre }}</span> • <span>{{ show.language }}</span>
              </p>
              <p class="mb-0">Available Tickets: {{ show.available_tickets }}</p>
              <p class="mb-0">Ticket Price: ₹{{ show.ticket_price }}</p>
              <p class="text-primary fw-semibold">{{ moment(show.showtime).format('LLLL') }}</p>
            </td>
            <td>{{ show.status }}</td>
            <td>
              <router-link class="btn btn-info btn-sm me-2" aria-current="page"
                :to="`/${show.id}/bookings`">Bookings</router-link>
              <router-link v-if="show.status === 'Finished'" class="btn btn-success btn-sm me-2" aria-current="page"
                :to="`/${show.id}/reviews`">Reviews</router-link>
              <button @click="deleteShow(show)" class="btn btn-danger btn-sm me-2">Delete</button>
              <button @click="editShow(show)" :class="{
                'btn btn-warning btn-sm me-1': show !== selectedShow,
                'btn btn-outline-warning btn-sm me-1': show === selectedShow
              }">
                Edit
              </button>
            </td>
          </tr>
        </tbody>

        <tbody v-else>
          <tr>
            <td colspan="4">No shows available.</td>
          </tr>
        </tbody>
        <input type="file" ref="fileInput" style="display: none;" @change="handleChangePoster($event, selectedShow)" />
      </table>
    </div>
  </div>
</template>

<script setup>
import api from '@/api';
import { computed, ref } from 'vue';
import moment from 'moment';

const props = defineProps({
  shows: {
    type: Array,
    required: true,
  },
  editMode: {
    type: Boolean,
    required: true,
  },
  show: {
    type: Object,
    required: true,
  },
  theaterId: {
    type: String,
    required: true,
  },
});

const selectedStatus = ref('All');
const filteredShows = computed(() => {
  if (selectedStatus.value === 'All') {
    return props.shows;
  } else {
    return props.shows.filter((show) => show.status === selectedStatus.value);
  }
});

const selectedShow = ref({});
const fileInput = ref(null);

const emits = defineEmits(['deleteShow', 'editShow', 'fetchShows']);

function changePoster(show) {
  selectedShow.value = show;
  if (fileInput.value) {
    fileInput.value.click();
  }
}

const handleChangePoster = async (event, show) => {
  const target = event.target;
  if (target.files && target.files.length > 0) {
    const formData = new FormData();
    formData.append('poster', target.files[0]);

    try {
      const response = await api.put(`/posters/${show.id}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      emits('fetchShows', props.theaterId);
      console.log('Poster Changed');
    } catch (error) {
      console.error(error);
    }
  }
};

function deleteShow(show) {
  emits('deleteShow', show);
}

function editShow(show) {
  emits('editShow', show);
  selectedShow.value = show;
}
</script>
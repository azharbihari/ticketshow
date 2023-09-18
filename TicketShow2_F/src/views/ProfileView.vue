<template>
    <main>
        <PageSpinner :isLoading="isLoadingPage" v-if="isLoadingPage" />
        <div class="container my-5" v-else>
            <MyAccountNav />
            <div class="row justify-content-sm-center mt-5 g-2" v-if="user">
                <div class="col-sm-2">
                    <input type="file" ref="avatarInput" class="d-none" @change="updateAvatar" />
                    <img :src="user.avatar" class="img-fluid img-thumbnail" @click="avatarInput && avatarInput.click()"
                        style="cursor: pointer;" :alt="user.first_name">
                    <p class="text-muted small mt-2">Click on the avatar to change it</p>
                </div>
                <div class="col-sm-6">
                    <div class="card">
                        <div class="card-header hstack gap-2">
                            <h5 class="card-title">{{ user.first_name }} {{ user.last_name }}</h5>
                            <div class="ms-auto">
                                <button type="submit" @click="updateProfile" v-if="isEditing"
                                    class="btn btn-primary btn-sm me-2">
                                    {{ isLoading ? 'Loading...' : 'Save' }}
                                </button>
                                <button type="button" @click="toggleEditing" class="btn btn-primary btn-sm">
                                    {{ isEditing ? 'Cancel' : 'Edit' }}
                                </button>
                            </div>
                        </div>
                        <div class="card-body" v-if="isEditing">
                            <form @submit.prevent="updateProfile">
                                <div class="row mb-3">
                                    <label for="firstName" class="col-sm-4 col-form-label">First Name</label>
                                    <div class="col-sm-8">
                                        <input type="text" class="form-control" v-model="user.first_name"
                                            placeholder="First Name" required id="firstName">
                                    </div>
                                </div>

                                <div class="row mb-3">
                                    <label for="lastName" class="col-sm-4 col-form-label">Last Name</label>
                                    <div class="col-sm-8">
                                        <input type="text" class="form-control" v-model="user.last_name"
                                            placeholder="Last Name" required id="lastName">
                                    </div>
                                </div>

                                <div class="row mb-3">
                                    <label for="dateOfBirth" class="col-sm-4 col-form-label">Date of Birth</label>
                                    <div class="col-sm-8">
                                        <input type="date" class="form-control" v-model="user.date_of_birth"
                                            placeholder="Date of Birth" required id="dateOfBirth">
                                    </div>
                                </div>

                                <div class="row mb-3">
                                    <label for="city" class="col-sm-4 col-form-label">City</label>
                                    <div class="col-sm-8">
                                        <select class="form-control" v-model="user.city" id="city">
                                            <option value="" disabled>Select City</option>
                                            <option v-for="theater in user.theaters" :value="theater.city"
                                                :key="theater.id">
                                                {{ theater.city }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </form>
                        </div>

                        <div class="card-body" v-else>
                            <div class="row g-2">
                                <div class="col-sm">
                                    <dl class="row">
                                        <dt class="col-sm-5">First Name</dt>
                                        <dd class="col-sm-7">{{ user.first_name }}</dd>

                                        <dt class="col-sm-5">Last Name</dt>
                                        <dd class="col-sm-7">{{ user.last_name }}</dd>

                                        <dt class="col-sm-5">City</dt>
                                        <dd class="col-sm-7">{{ user.city }}</dd>

                                        <dt class="col-sm-5">Date of Birth</dt>
                                        <dd class="col-sm-7">{{ moment(user.date_of_birth).format('LL') }}</dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import moment from 'moment';
import MyAccountNav from '@/components/MyAccountNav.vue';

const user = ref({});
const avatarInput = ref(null);
const isLoading = ref(false);
const isEditing = ref(false);
const isLoadingPage = ref(true);

onMounted(async () => {
    await fetchProfile();
});

async function fetchProfile() {
    try {
        isLoadingPage.value = true;
        const response = await api.get('/profile');
        if (response.status === 200) {
            user.value = response.data;
        } else {
            console.error('Failed to fetch profile');
        }
    } catch (error) {
        console.error('Failed to fetch profile');
    } finally {
        isLoadingPage.value = false;
    }
}

async function updateAvatar() {
    const avatar = avatarInput.value?.files?.[0];
    if (avatar) {
        const formData = new FormData();
        formData.append('avatar', avatar);
        try {
            const response = await api.put('/avatar', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            fetchProfile();
            console.log('Avatar Updated');
        } catch (error) {
            console.error('Error uploading avatar:', error);
        }
    }
}

async function updateProfile() {
    isLoading.value = true;
    try {
        const response = await api.put('/profile', user.value);
        if (response.status === 200) {
            console.log('Profile updated');
            isEditing.value = false;
            isLoading.value = false;
        } else {
            console.error('Failed to update profile');
        }
    } catch (error) {
        console.error(error);
    }
}

function toggleEditing() {
    isEditing.value = !isEditing.value;
}
</script>

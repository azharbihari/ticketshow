<template>
  <main>
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <h1>Register</h1>
          <form @submit.prevent="handleRegistration(user)" class="w-75">
            <div class="row mb-3">
              <div class="col-md-6">
                <label for="first_name" class="form-label">First Name</label>
                <input type="text" class="form-control" id="first_name" v-model="user.first_name"
                  placeholder="Enter your first name" required>
              </div>
              <div class="col-md-6">
                <label for="last_name" class="form-label">Last Name</label>
                <input type="text" class="form-control" id="last_name" v-model="user.last_name"
                  placeholder="Enter your last name" required>
              </div>
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Email</label>
              <input type="text" class="form-control" id="email" v-model="user.email" placeholder="Enter your email"
                required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" class="form-control" id="password" v-model="user.password"
                placeholder="Enter your password" required>
            </div>
            <div class="mb-3">
              <label for="confirm_password" class="form-label">Confirm Password</label>
              <input
                :class="{ 'form-control is-invalid': user.confirm_password !== user.password, 'form-control': user.confirm_password === user.password }"
                type="password" id="confirm_password" v-model="user.confirm_password" placeholder="Confirm your password"
                required aria-describedby="confirmPasswordFeedback">

              <div id="confirmPasswordFeedback" class="invalid-feedback">
                Passwords do not match
              </div>
            </div>

            <button type="submit" class="btn btn-primary" :disabled="isLoading">
              {{ isLoading ? 'Loading...' : 'Register' }}
            </button>
          </form>

          <p class="fw-bold mt-3">Already registered? <RouterLink class="icon-link icon-link-hover" aria-current="page"
              to="/login">Login</RouterLink>.</p>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { ref } from 'vue';

const authStore = useAuthStore();
const user = ref({});

const isLoading = ref(false);

async function handleRegistration(user) {
  if (user.password !== user.confirm_password) {
    console.error('Passwords do not match');
    return;
  }

  isLoading.value = true;

  try {
    await authStore.register(user);
    resetForm();
  } catch (error) {
    console.error('Registration failed', error);
  } finally {
    isLoading.value = false;
  }
}

function resetForm() {
  user.value = {};
}
</script>

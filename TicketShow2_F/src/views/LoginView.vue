<template>
  <main>
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <h1>Login</h1>
          <form @submit.prevent="handleLogin(user)" class="w-75">

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
            
            <button type="submit" class="btn btn-primary" :disabled="isLoading" >{{ isLoading ? 'Loading...' : 'Log In' }}</button>
          </form>

          <p class="fw-bold mt-3"> Don't have an account? <RouterLink class="icon-link icon-link-hover" aria-current="page" to="/register">Click here to create one</RouterLink>. </p>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { ref } from 'vue';

const authStore = useAuthStore();
const user = ref({ email: '', password: '' });

const isLoading = ref(false);

async function handleLogin() {
  isLoading.value = true;
  try {
    await authStore.login(user.value);
    resetForm();
  } catch (error) {
    console.error('Login failed', error);
  } finally {
    isLoading.value = false;
  }
}

function resetForm() {
  user.value = { email: '', password: '' };
}
</script>
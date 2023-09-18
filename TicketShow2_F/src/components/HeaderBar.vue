<template>
  <header>
  <nav class="container navbar navbar-expand-lg bg-body-tertiary">
    <div class="container">
      <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#navbarOffcanvasLg" aria-controls="navbarOffcanvasLg" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>


      <RouterLink class="navbar-brand ms-2 ms-sm-0" aria-current="page" to="/"><img src="@/assets/logo.svg" alt="TicketShow" width="30" height="30"></RouterLink>

      <div class="offcanvas offcanvas-start" tabindex="-1" id="navbarOffcanvasLg" aria-labelledby="navbarOffcanvasLgLabel">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasNavbarLabel">TicketShow</h5>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>

        <div class="offcanvas-body">
          <ul class="navbar-nav justify-content-start flex-grow-1 pe-3">
            <li class="nav-item" data-bs-dismiss="offcanvas">
              <RouterLink class="nav-link" aria-current="page" to="/">Home</RouterLink>
            </li>

            <li class="nav-item" data-bs-dismiss="offcanvas" v-if="isAuthenticated && isAdmin">
              <RouterLink class="nav-link" aria-current="page" to="/dashboard">Dashboard</RouterLink>
            </li>

            <li class="nav-item" data-bs-dismiss="offcanvas" v-if="isAuthenticated && isAdmin">
                <RouterLink class="nav-link" aria-current="page" to="/insights">Insights</RouterLink>
            </li>
          </ul>
        </div>
      </div>

      <div class="dropdown ms-auto" v-if="isAuthenticated && user">
           <a href="#" data-bs-toggle="dropdown" aria-expanded="false"
              class="text-decoration-none dropdown-toggle badge d-flex align-items-center p-1 pe-2 text-warning-emphasis bg-success-subtle border border-warning-subtle rounded-pill">
              <img :src="user.avatar" :alt="user.first_name" width="24" height="24" class="rounded-circle me-1"> {{ user.first_name }} {{user.last_name }}
           </a>


          <ul class="dropdown-menu dropdown-menu-end">
            <li>
              <RouterLink class="dropdown-item" aria-current="page" to="/mybookings">My Bookings</RouterLink>
            </li>
            <li>
              <RouterLink class="dropdown-item" aria-current="page" to="/profile">Profile</RouterLink>
            </li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li @click="authStore.logout"><a class="dropdown-item" href="#">Log out</a></li>
          </ul>
      </div>

      <div class="ms-auto" v-else>
          <RouterLink class="btn btn-primary btn-sm me-1" aria-current="page" to="/login">Login</RouterLink>
          <RouterLink class="btn btn-outline-secondary btn-sm" aria-current="page" to="/register">Register</RouterLink>
      </div>
    </div>
  </nav>
  </header>
</template>



<script setup>
import { useAuthStore } from '@/stores/auth';
import { storeToRefs } from 'pinia';

const authStore = useAuthStore();
const { user, isAdmin, isAuthenticated } = storeToRefs(authStore)

</script>
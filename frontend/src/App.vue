<template>
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <RouterLink to="/" class="navbar-item"><strong>JobHunt</strong></RouterLink>
      </div>

      <div class="navbar-menu">
        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <!-- Show Create Job for company users -->
              <template v-if="$store.state.isAuthenticated && $store.state.userProfile?.user_type === 'company'">
                <RouterLink to="/create-job" class="button is-success">Create Job</RouterLink>
                <!-- Link to applications list for company users -->
                <RouterLink to="/applications" class="button is-info">Applications</RouterLink>
              </template>
              
              <!-- Show My Account if logged in -->
              <template v-if="$store.state.isAuthenticated">
                <RouterLink to="/my-account" class="button is-light">My Account</RouterLink>
              </template>
              
              <!-- Show Sign Up / Log In if NOT logged in -->
              <template v-else>
                <RouterLink to="/sign-up" class="button is-primary"><strong>Sign Up</strong></RouterLink>
                <RouterLink to="/log-in" class="button is-light">Log In</RouterLink>
              </template>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <section class="section">
      <RouterView />
    </section>

    <footer class="footer">
      <p class="content has-text-centered">Copyright (c) 2026 EIE3117 G17 JobHunt</p>
    </footer>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.token
    if (token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
  }
}
</script>

<style lang="scss">
@import '../node_modules/bulma';
</style>

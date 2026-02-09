<template>
  <div class="page-my-account">
    <div class="columns">
      <div class="column is-6 is-offset-3">
        <h1 class="title">My Account</h1>
        
        <div class="box">
          <h2 class="subtitle">User Info</h2>
          <p><strong>Status:</strong> {{ isAuthenticated ? 'Logged In' : 'Logged Out' }}</p>
          <button @click="logout" class="button is-danger">Log Out</button>
        </div>

        <!-- Company User: Create Jobs -->
        <div v-if="userType === 'company'" class="box">
          <RouterLink to="/create-job" class="button is-primary is-fullwidth">
            Create New Job
          </RouterLink>
        </div>

        <!-- Individual User: View Jobs -->
        <div v-if="userType === 'individual'" class="box">
          <RouterLink to="/jobs" class="button is-primary is-fullwidth">
            Browse Jobs
          </RouterLink>
        </div>

        <div v-if="userType === 'company'" class="box">
         <RouterLink to="/create-job" class="button is-primary is-fullwidth">
           Create New Job
         </RouterLink>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MyAccount',
  data() {
    return {
      userType: 'individual'  // From your backend later
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store.state.isAuthenticated
    }
  },
  mounted() {
    document.title = 'My Account - JobHunt'
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      this.$store.commit('removeToken')
      axios.defaults.headers.common['Authorization'] = ''
      this.$router.push('/')
    }
  }
}
</script>

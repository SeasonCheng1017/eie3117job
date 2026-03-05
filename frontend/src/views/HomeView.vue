<template>
  <div class="home">
    <section class="hero is-medium is-dark mb-6">
      <div class="hero-body has-text-centered">
        <p class="title mb-6">Welcome to JobHunt</p>
        <p class="subtitle">Find your dream job or hire top talent</p>
      </div>
    </section>

    <!-- Latest Jobs Section -->
    <section class="section">
      <div class="container">
        <h2 class="title">Latest Jobs</h2>
        <div v-if="latestJobs.length > 0" class="columns is-multiline">
          <div v-for="job in latestJobs" :key="job.id" class="column is-4">
            <div class="box">
              <h3 class="title is-5">{{ job.title }}</h3>
              <p><strong>Location:</strong> {{ job.location }}</p>
              <p><strong>Salary:</strong> {{ job.salary }}</p>
              <p class="mt-3">{{ job.requirement }}</p>
              <RouterLink 
                :to="`/jobs/${job.id}`" 
                class="button is-primary mt-3 is-fullwidth">
                View Details
              </RouterLink>
            </div>
          </div>
        </div>
        <div v-else class="notification is-info">
          <p>No jobs available at the moment.</p>
        </div>
        <div class="has-text-centered mt-6">
          <RouterLink to="/jobs" class="button is-dark is-large">
            View All Jobs
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HomeView',
  data() {
    return {
      latestJobs: []
    }
  },
  mounted() {
    document.title = 'JobHunt - Home'
    this.fetchLatestJobs()
  },
  methods: {
    fetchLatestJobs() {
      // Fetch latest 6 jobs from the API
      axios.get('/api/v1/jobs/')
        .then(response => {
          // Get the first 6 jobs
          this.latestJobs = response.data.slice(0, 6)
        })
        .catch(error => {
          console.error('Failed to fetch jobs:', error)
        })
    }
  }
}
</script>

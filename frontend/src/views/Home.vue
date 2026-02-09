<template>
  <section class="hero is-medium is-dark mb-6">
    <div class="hero-body has-text-centered">
      <p class="title mb-6">Find Your Next Job</p>
      <p class="subtitle">Connect companies and individuals</p>
    </div>
  </section>

  <div class="columns is-multiline">
    <div class="column is-12">
      <h2 class="is-size-2 has-text-centered">Latest Jobs</h2>
    </div>

    <div class="column is-3" v-for="job in latestJobs" :key="job.id">
      <div class="box">
        <h3 class="is-size-4">{{ job.title }}</h3>
        <p class="is-size-6 has-text-grey">
          {{ job.company.company_name || job.company.nickname }} · {{ job.location }}
        </p>
        <p class="is-size-6 has-text-grey">Salary: {{ job.salary }}</p>
        <!-- later we’ll turn this into a RouterLink to JobDetail -->
        <button class="button is-dark">View details</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data() {
    return {
      latestJobs: [],
    }
  },
  methods: {
    getLatestJobs() {
      axios
        .get('/api/v1/jobs/')
        .then((response) => {
          this.latestJobs = response.data
        })
        .catch((error) => {
          console.error(error)
        })
    },
  },
  mounted() {
    document.title = 'Home | JobHunter'
    this.getLatestJobs()
  },
}
</script>

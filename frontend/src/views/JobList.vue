<template>
  <div class="page-job-list">
    <div class="columns">
      <div class="column is-10 is-offset-1">
        <h1 class="title">All Jobs</h1>

        <table class="table is-fullwidth is-striped">
          <thead>
            <tr>
              <th>Title</th>
              <th>Requirement</th>
              <th>Duty</th>
              <th>Salary</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="job in jobs" :key="job.id">
              <td>{{ job.title }}</td>
              <td>{{ job.requirement }}</td>
              <td>{{ job.duty }}</td>
              <td>{{ job.salary }}</td>
              <td>
                <RouterLink
                  class="button is-small is-link"
                  :to="`/jobs/${job.id}`"
                >
                  View
                </RouterLink>
              </td>
            </tr>
          </tbody>
        </table>

        <p v-if="!jobs.length">No jobs available yet.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'JobList',
  data() {
    return {
      jobs: []
    }
  },
  mounted() {
    document.title = 'Job List - JobHunt'
    this.fetchJobs()
  },
  methods: {
    fetchJobs() {
      axios.get('/api/v1/jobs/')
        .then(response => {
          this.jobs = response.data
        })
        .catch(error => {
          console.error('Failed to fetch jobs:', error)
        })
    }
  }
}
</script>

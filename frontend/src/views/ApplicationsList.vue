<template>
  <div class="page-applications">
    <div class="columns">
      <div class="column is-10 is-offset-1">
        <h1 class="title">Received Applications</h1>

        <table class="table is-fullwidth is-striped" v-if="applications.length">
          <thead>
            <tr>
              <th>Job</th>
              <th>Applicant</th>
              <th>Message</th>
              <th>CV</th>
              <th>Date</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in applications" :key="app.id">
              <td>{{ app.job.title }}</td>
              <td>{{ app.applicant.nickname || app.applicant.user.username }}</td>
              <td>{{ app.message }}</td>
              <td>
                <a :href="app.cv" target="_blank" rel="noopener" class="button is-small is-info">
                  Download
                </a>
              </td>
              <td>{{ formatDate(app.created_at) }}</td>
              <td>{{ app.status }}</td>
              <td>
                <RouterLink :to="`/applications/${app.id}`" class="button is-small is-link">
                  View
                </RouterLink>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="!applications.length" class="notification is-info">
          No applications received yet.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ApplicationsList',
  data() {
    return {
      applications: []
    }
  },
  mounted() {
    document.title = 'Applications - JobHunt'
    if (this.$store.state.userProfile?.user_type !== 'company') {
      // redirect non-company users
      this.$router.push('/')
      return
    }
    this.fetchApplications()
  },
  methods: {
    fetchApplications() {
      axios.get('/api/v1/applications/')
        .then(response => {
          this.applications = response.data
        })
        .catch(error => {
          console.error('Failed to load applications', error)
        })
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString()
    }
  }
}
</script>

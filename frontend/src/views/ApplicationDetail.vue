<template>
  <div class="page-application-detail">
    <div class="columns">
      <div class="column is-8 is-offset-2">
        <h1 class="title">Application Details</h1>

        <div v-if="application">
          <p><strong>Job:</strong> {{ application.job.title }}</p>
          <p><strong>Applicant:</strong> {{ application.applicant.nickname || application.applicant.user.username }}</p>
          <p><strong>Message:</strong></p>
          <p>{{ application.message }}</p>
          <p><strong>Submitted:</strong> {{ formatDate(application.created_at) }}</p>
          <p><strong>Status:</strong> {{ application.status }}</p>
          <p>
            <strong>CV:</strong>
            <a :href="application.cv" target="_blank" rel="noopener">Download</a>
          </p>

          <div class="field">
            <label class="label">Update status</label>
            <div class="control">
              <div class="select">
                <select v-model="newStatus">
                  <option value="pending">Pending</option>
                  <option value="accepted">Accepted</option>
                  <option value="rejected">Rejected</option>
                </select>
              </div>
            </div>
          </div>

          <div class="field">
            <button class="button is-primary" :disabled="updating" @click="updateStatus">
              {{ updating ? 'Saving...' : 'Save' }}
            </button>
          </div>
        </div>

        <div v-else class="notification is-warning">
          Loading application...
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ApplicationDetail',
  data() {
    return {
      application: null,
      newStatus: '',
      updating: false
    }
  },
  mounted() {
    if (this.$store.state.userProfile?.user_type !== 'company') {
      this.$router.push('/')
      return
    }
    this.loadApplication()
    document.title = 'Application - JobHunt'
  },
  methods: {
    loadApplication() {
      const id = this.$route.params.id
      axios.get(`/api/v1/applications/${id}/`)
        .then(response => {
          this.application = response.data
          this.newStatus = this.application.status
        })
        .catch(error => console.error('Failed to load application', error))
    },
    updateStatus() {
      if (this.newStatus === this.application.status) return
      this.updating = true
      const id = this.$route.params.id
      axios.patch(`/api/v1/applications/${id}/`, { status: this.newStatus })
        .then(response => {
          this.application = response.data
        })
        .catch(error => console.error('Failed to update status', error))
        .finally(() => { this.updating = false })
    },
    formatDate(str) {
      return new Date(str).toLocaleString()
    }
  }
}
</script>

<template>
  <div class="page-create-job">
    <div class="columns">
      <div class="column is-6 is-offset-3">
        <h1 class="title">Create Job</h1>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label class="label">Job Title</label>
            <div class="control">
              <input class="input" v-model="title" required>
            </div>
          </div>

          <div class="field">
            <label class="label">Location</label>
            <div class="control">
              <input class="input" v-model="location" required>
            </div>
          </div>

          <div class="field">
            <label class="label">Job Requirement</label>
            <div class="control">
              <textarea class="textarea" v-model="requirement" required></textarea>
            </div>
          </div>

          <div class="field">
            <label class="label">Job Duty</label>
            <div class="control">
              <textarea class="textarea" v-model="duty" required></textarea>
            </div>
          </div>

          <div class="field">
            <label class="label">Salary</label>
            <div class="control">
              <input class="input" v-model="salary" required>
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" :key="error">{{ error }}</p>
          </div>

          <div class="field">
            <button class="button is-primary is-fullwidth" :disabled="submitting">
              {{ submitting ? 'Creating...' : 'Create Job' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CreateJob',
  data() {
    return {
      title: '',
      location: '',
      requirement: '',
      duty: '',
      salary: '',
      errors: [],
      submitting: false
    }
  },
  mounted() {
    document.title = 'Create Job - JobHunt'
    // Check if user is authenticated and is a company
    if (!this.$store.state.isAuthenticated) {
      this.$router.push('/log-in?to=/create-job')
      return
    }
    if (this.$store.state.userProfile?.user_type !== 'company') {
      alert('Only company users can create jobs.')
      this.$router.push('/')
    }
  },
  methods: {
    submitForm() {
      this.errors = []
      this.submitting = true

      const payload = {
        title: this.title,
        location: this.location,
        requirement: this.requirement,
        duty: this.duty,
        salary: this.salary,
        is_open: true
      }

      axios.post('/api/v1/jobs/', payload)
        .then(() => {
          alert('Job created successfully!')
          this.$router.push('/jobs')
        })
        .catch(error => {
          if (error.response?.data) {
            for (const property in error.response.data) {
              const messages = Array.isArray(error.response.data[property]) 
                ? error.response.data[property] 
                : [error.response.data[property]]
              messages.forEach(msg => {
                this.errors.push(`${property}: ${msg}`)
              })
            }
          } else {
            this.errors.push('Something went wrong. Please try again.')
            console.error(error)
          }
        })
        .finally(() => {
          this.submitting = false
        })
    }
  }
}
</script>

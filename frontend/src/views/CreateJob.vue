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
            <button class="button is-primary is-fullwidth">Create Job</button>
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
      requirement: '',
      duty: '',
      salary: '',
      errors: []
    }
  },
  mounted() {
    document.title = 'Create Job - JobHunt'
  },
  methods: {
    submitForm() {
      this.errors = []

      const payload = {
        title: this.title,
        requirement: this.requirement,
        duty: this.duty,
        salary: this.salary
      }

      axios.post('http://localhost:8000/api/v1/jobs/', payload)
        .then(() => {
          alert('Job created!')
          this.$router.push('/jobs')
        })
        .catch(error => {
          if (error.response?.data) {
            for (const property in error.response.data) {
              this.errors.push(`${property}: ${error.response.data[property]}`)
            }
          } else {
            this.errors.push('Something went wrong. Please try again.')
          }
        })
    }
  }
}
</script>

<script>
import axios from 'axios'

export default {
  name: 'JobDetail',
  data() {
    return {
      job: null,
      message: '',
      cvFile: null,
      submitting: false,
      success: false,
      error: '',
    }
  },
  methods: {
    getJob() {
      const id = this.$route.params.id
      axios
        .get(`/api/v1/jobs/${id}/`)
        .then((response) => {
          this.job = response.data
          document.title = this.job.title + ' | JobHunter'
        })
        .catch((error) => console.error(error))
    },
    onFileChange(e) {
      this.cvFile = e.target.files[0]
    },
    submitApplication() {
      if (!this.cvFile || !this.message) {
        this.error = 'Please provide a message and upload your CV.'
        return
      }
      
      if (!this.$store.state.isAuthenticated) {
        this.error = 'You must be logged in to apply.'
        return
      }
      
      this.submitting = true
      this.error = ''
      this.success = false

      const id = this.$route.params.id
      const formData = new FormData()
      formData.append('message', this.message)
      formData.append('cv', this.cvFile)

      axios
        .post(`/api/v1/jobs/${id}/apply/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        .then(() => {
          this.success = true
          this.message = ''
          this.cvFile = null
        })
        .catch((error) => {
          console.error(error)
          this.error = error.response?.data?.detail || 'Failed to submit application.'
        })
        .finally(() => {
          this.submitting = false
        })
    },
  },
  mounted() {
    this.getJob()
  },
}
</script>

<template>
  <section class="section" v-if="job">
    <div class="container">
      <h1 class="title">{{ job.title }}</h1>
      <h2 class="subtitle">
        <strong>Employer:</strong> {{ job.company.company_name || job.company.nickname }}
      </h2>

      <p><strong>Work Place:</strong> {{ job.location }}</p>

      <p><strong>Salary:</strong> {{ job.salary }}</p>

      <p class="mt-4"><strong>Requirement</strong></p>
      <p>{{ job.requirement }}</p>

      <p class="mt-4"><strong>Duty</strong></p>
      <p>{{ job.duty }}</p>

      <hr class="my-5" />

      <h2 class="subtitle">Apply for this job</h2>

      <div v-if="error" class="notification is-danger">{{ error }}</div>
      <div v-if="success" class="notification is-success">
        Application submitted successfully.
      </div>

      <div class="field">
        <label class="label">Message</label>
        <div class="control">
          <textarea
            class="textarea"
            v-model="message"
            placeholder="Introduce yourself, skills, etc."
          ></textarea>
        </div>
      </div>

      <div class="field">
        <label class="label">CV (PDF / DOC)</label>
        <div class="control">
          <input type="file" class="input" @change="onFileChange" />
        </div>
      </div>

      <div class="field mt-4">
        <div class="control">
          <button
            class="button is-dark"
            :disabled="submitting"
            @click="submitApplication"
          >
            {{ submitting ? 'Submitting...' : 'Submit Application' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

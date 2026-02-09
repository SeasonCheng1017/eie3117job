<template>
  <div class="page-log-in">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Log In</h1>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label class="label">Username</label>
            <div class="control">
              <input type="text" class="input" v-model="username" required>
            </div>
          </div>

          <div class="field">
            <label class="label">Password</label>
            <div class="control">
              <input type="password" class="input" v-model="password" required>
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" :key="error">{{ error }}</p>
          </div>

          <div class="field">
            <div class="control">
              <button class="button is-dark is-fullwidth">Log In</button>
            </div>
          </div>
        </form>
        
        <hr>
        <p>Don't have an account? <RouterLink to="/sign-up">Sign Up</RouterLink></p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LogIn',
  data() {
    return {
      username: '',
      password: '',
      errors: []
    }
  },
  mounted() {
    document.title = 'Log In - JobHunt'
  },
  methods: {
    submitForm() {
      this.errors = []
      
      axios.post('/api/v1/token/login/', {
        username: this.username,
        password: this.password
      })
      .then(response => {
        const token = response.data.auth_token
        
        this.$store.commit('setToken', token)
        
        axios.defaults.headers.common['Authorization'] = "Token " + token
        localStorage.setItem('token', token)
        
        alert('Logged in successfully!')
        
        // Redirect to where they came from or home
        const toPath = this.$route.query.to || '/'
        this.$router.push(toPath)
      })
      .catch(error => {
        if (error.response) {
          for (const property in error.response.data) {
            this.errors.push(`${property}: ${error.response.data[property]}`)
          }
        } else {
          this.errors.push('Something went wrong. Please try again.')
          console.log(JSON.stringify(error))
        }
      })
    }
  }
}
</script>

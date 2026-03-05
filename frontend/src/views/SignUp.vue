<template>
  <div class="page-sign-up">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Sign Up</h1>
        
        <form @submit.prevent="submitForm">
          <!-- User Type (Required by Spec) -->
          <div class="field">
            <label class="label"><strong>Sign up as:</strong></label>
            <div class="control">
              <label class="radio" style="display: block; margin-bottom: 0.5rem;">
                <input type="radio" v-model="form.user_type" value="individual" name="user_type">
                <span style="margin-left: 0.5rem;">Job Seeker (Individual)</span>
              </label>
              <label class="radio" style="display: block;">
                <input type="radio" v-model="form.user_type" value="company" name="user_type">
                <span style="margin-left: 0.5rem;">Employer (Company)</span>
              </label>
            </div>
          </div>

          <!-- Login ID / Username -->
          <div class="field">
            <label class="label">Login ID (Username)</label>
            <div class="control">
              <input type="text" class="input" v-model="form.username" required>
            </div>
          </div>

          <!-- Nickname -->
          <div class="field">
            <label class="label">Nickname</label>
            <div class="control">
              <input type="text" class="input" v-model="form.nickname" required>
            </div>
          </div>

          <!-- Email -->
          <div class="field">
            <label class="label">Email</label>
            <div class="control">
              <input type="email" class="input" v-model="form.email" required>
            </div>
          </div>

          <!-- Password -->
          <div class="field">
            <label class="label">Password</label>
            <div class="control">
              <input type="password" class="input" v-model="form.password" required>
            </div>
          </div>

          <!-- Password Confirmation -->
          <div class="field">
            <label class="label">Confirm Password</label>
            <div class="control">
              <input type="password" class="input" v-model="form.password_retype" required>
            </div>
          </div>
          
          <!-- Profile Image -->
          <div class="field">
            <label class="label">Profile Image</label>
            <div class="control">
              <input type="file" class="input" @change="onFileChange" accept="image/*">
           </div>
          </div>

          <!-- Errors -->
          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" :key="error">{{ error }}</p>
          </div>

          <div class="field">
            <div class="control">
              <button class="button is-dark is-fullwidth">Sign Up</button>
            </div>
          </div>
        </form>

        <hr>
        <RouterLink to="/log-in">Log In</RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SignUp',
  data() {
    return {
      form: {
        username: '',
        password: '',
        password_retype: '',
        email: '',
        nickname: '',
        user_type: 'individual'
      },
      profileImage: null,   // store File object
      errors: []
    }
  },
  mounted() {
    document.title = 'Sign Up - JobHunt'
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0]
      this.profileImage = file || null
    },
    submitForm() {
      this.errors = []

      const formData = new FormData()
      formData.append('username', this.form.username)
      formData.append('password', this.form.password)
      // djoser expects `re_password` for confirmation
      formData.append('re_password', this.form.password_retype)
      formData.append('email', this.form.email)
      formData.append('nickname', this.form.nickname)
      formData.append('user_type', this.form.user_type)
      if (this.profileImage) {
        formData.append('profile_image', this.profileImage)
      }

      axios.post('/api/v1/users/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      .then(() => {
        alert('Account created! Please log in.')
        this.$router.push('/log-in')
      })
      .catch(error => {
        if (error.response?.data) {
          for (const property in error.response.data) {
            // hide internal re_password field and rename for display
            if (property === 're_password') {
              const messages = Array.isArray(error.response.data[property])
                ? error.response.data[property]
                : [error.response.data[property]]
              messages.forEach(msg => {
                this.errors.push(`Password confirmation: ${msg}`)
              })
              continue
            }
            const friendlyName = property === 'password' ? 'Password' : property
            const messages = Array.isArray(error.response.data[property])
              ? error.response.data[property]
              : [error.response.data[property]]
            messages.forEach(msg => {
              // convert some common password validator messages
              let text = msg
              if (/too common/i.test(msg) || /entirely numeric/i.test(msg)) {
                text = 'Weak password. Choose a stronger combination (letters and numbers).'
              }
              this.errors.push(`${friendlyName}: ${text}`)
            })
          }
          console.log(JSON.stringify(error.response.data))
        } else if (error.message) {
          this.errors.push('Something went wrong. Please try again.')
        }
      })
    }
  }
}
</script>

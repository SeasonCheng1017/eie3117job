<template>
  <div class="page-my-account">
    <div class="columns">
      <div class="column is-6 is-offset-3">
        <h1 class="title">My Account</h1>
        
        <!-- Profile Card -->
        <div class="box">
          <div class="columns">
            <div class="column is-4">
              <!-- Profile Image -->
              <div class="image is-128x128">
                <img 
                  v-if="profileImage" 
                  :src="profileImage" 
                  alt="Profile Picture"
                  style="border-radius: 8px;"
                >
                <div v-else style="width: 128px; height: 128px; background-color: #f5f5f5; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #999;">
                  No image
                </div>
              </div>
            </div>
            
            <div class="column is-8">
              <h2 class="subtitle">Profile Information</h2>
              <p><strong>Username:</strong> {{ user?.username || 'Loading...' }}</p>
              <p><strong>Email:</strong> {{ user?.email || 'Loading...' }}</p>
              <p><strong>Nickname:</strong> {{ userProfile?.nickname || 'Not set' }}</p>
              <p><strong>Account Type:</strong> 
                <span v-if="userProfile?.user_type === 'company'" class="tag is-info">Employer</span>
                <span v-else-if="userProfile?.user_type === 'individual'" class="tag is-success">Job Seeker</span>
                <span v-else class="tag">Unknown</span>
              </p>
              <p v-if="userProfile?.user_type === 'company'"><strong>Company Name:</strong> {{ userProfile?.company_name || 'Not set' }}</p>
              <p v-if="userProfile?.user_type === 'company'"><strong>Website:</strong> {{ userProfile?.website || 'Not set' }}</p>
              <button @click="logout" class="button is-danger mt-4">Log Out</button>
            </div>
          </div>
        </div>

        <!-- Company User: Create Jobs -->
        <div v-if="userProfile?.user_type === 'company'" class="box">
          <RouterLink to="/create-job" class="button is-primary is-fullwidth">
            Create New Job
          </RouterLink>
        </div>

        <!-- Company User: View Applications -->
        <div v-if="userProfile?.user_type === 'company'" class="box">
          <RouterLink to="/applications" class="button is-info is-fullwidth">
            View Applications
          </RouterLink>
        </div>

        <!-- Individual User: View Jobs -->
        <div v-if="userProfile?.user_type === 'individual'" class="box">
          <RouterLink to="/jobs" class="button is-primary is-fullwidth">
            Browse Jobs
          </RouterLink>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MyAccount',
  data() {
    return {
      user: null,
      userProfile: null,
      profileImage: null
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store.state.isAuthenticated
    }
  },
  mounted() {
    document.title = 'My Account - JobHunt'
    if (!this.isAuthenticated) {
      this.$router.push('/log-in?to=/my-account')
      return
    }
    
    if (this.$store.state.user && this.$store.state.userProfile) {
      this.user = this.$store.state.user
      this.userProfile = this.$store.state.userProfile
      this.loadProfileImage()
    } else {
      // load user details if store doesn't have them yet
      this.$store.dispatch('loadUser').then(() => {
        this.user = this.$store.state.user
        this.userProfile = this.$store.state.userProfile
        this.loadProfileImage()
      })
    }
  },
  methods: {
    loadProfileImage() {
      if (this.userProfile?.profile_image) {
        // Profile image could be a full URL or a relative path
        // If it's not a full URL, prepend the server address
        if (this.userProfile.profile_image.startsWith('http')) {
          this.profileImage = this.userProfile.profile_image
        } else {
          this.profileImage = `http://localhost:8000${this.userProfile.profile_image}`
        }
      }
    },
    logout() {
      // Optional: Logout endpoint
      axios.post('/api/v1/token/logout/')
        .catch(error => console.error('Logout error:', error))
        .finally(() => {
          localStorage.removeItem('token')
          // clear cookie
          document.cookie = 'token=; Max-Age=0; path=/'
          this.$store.commit('removeToken')
          axios.defaults.headers.common['Authorization'] = ''
          this.$router.push('/')
        })
    }
  }
}
</script>

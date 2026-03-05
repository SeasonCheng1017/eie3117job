import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000'

// Add token to every request if it exists
axios.interceptors.request.use(
  (config) => {
    // prefer cookie token which is more persistent
    const token = localStorage.getItem('token') || document.cookie.match(/(?:^|; )token=([^;]+)/)?.[1]
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

const app = createApp(App)

app.use(store)
store.commit('initializeStore')

// if we already have a token, fetch the current user
if (store.state.isAuthenticated) {
  store.dispatch('loadUser')
}

app.use(router)
app.mount('#app')   


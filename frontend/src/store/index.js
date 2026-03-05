import { createStore } from 'vuex'
import { getCookie, setCookie, deleteCookie } from '../utils/cookies'
import axios from 'axios'

export default createStore({
  state: {
    token: '',
    isAuthenticated: false,
    user: null,
    userProfile: null
  },
  mutations: {
    initializeStore(state) {
      // read from localStorage first then cookie as fallback
      let token = localStorage.getItem('token') || getCookie('token')
      if (token) {
        state.token = token
        state.isAuthenticated = true
        // make sure localStorage has it for quick lookup
        localStorage.setItem('token', token)
      } else {
        state.token = ''
        state.isAuthenticated = false
      }
    },
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
      localStorage.setItem('token', token)
      setCookie('token', token, 30)
    },
    setUser(state, user) {
      state.user = user
    },
    setUserProfile(state, profile) {
      state.userProfile = profile
    },
    removeToken(state) {
      state.token = ''
      state.isAuthenticated = false
      state.user = null
      state.userProfile = null
      localStorage.removeItem('token')
      deleteCookie('token')
    }
  },
  actions: {
    loadUser({ commit }) {
      return axios.get('/api/v1/users/me/')
        .then(response => {
          commit('setUser', response.data)
          if (response.data.profile) {
            commit('setUserProfile', response.data.profile)
          }
        })
        .catch(error => {
          console.error('Failed to load user:', error)
        })
    }
  },
  modules: {}
})

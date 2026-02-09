import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import LogIn from '../views/LogIn.vue'
import SignUp from '../views/SignUp.vue'
import MyAccount from '../views/MyAccount.vue'
import CreateJob from '../views/CreateJob.vue'
import JobList from '../views/JobList.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/about', name: 'about', component: AboutView },
    { path: '/log-in', name: 'log-in', component: LogIn },
    { path: '/sign-up', name: 'sign-up', component: SignUp },
    { path: '/my-account', name: 'my-account', component: MyAccount },
    { path: '/create-job', name: 'create-job', component: CreateJob },
    { path: '/jobs', name: 'jobs', component: JobList }
  ]
})

export default router

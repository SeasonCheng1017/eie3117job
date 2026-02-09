<template>
  <div class="page-job-list">
    <div class="columns">
      <div class="column is-10 is-offset-1">
        <h1 class="title">All Jobs</h1>

        <table class="table is-fullwidth is-striped">
          <thead>
            <tr>
              <th>Title</th>
              <th>Requirement</th>
              <th>Duty</th>
              <th>Salary</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="job in jobs" :key="job.id">
              <td>{{ job.title }}</td>
              <td>{{ job.requirement }}</td>
              <td>{{ job.duty }}</td>
              <td>{{ job.salary }}</td>
              <td>
                <RouterLink
                  class="button is-small is-link"
                  :to="`/jobs/${job.id}`"
                >
                  View
                </RouterLink>
              </td>
            </tr>
          </tbody>
        </table>

        <p v-if="!jobs.length">No jobs available yet.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'JobList',
  data() {
    return {
      jobs: [
        {
          id: 1,
          title: 'Frontend Developer',
          requirement: 'Vue.js, HTML, CSS',
          duty: 'Build UI components',
          salary: 'HKD 25,000'
        },
        {
          id: 2,
          title: 'Backend Developer',
          requirement: 'Django, REST API',
          duty: 'Develop APIs and business logic',
          salary: 'HKD 28,000'
        }
      ]
    }
  },
  mounted() {
    document.title = 'Job List - JobHunt'
  }
}
</script>

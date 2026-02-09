<template>
  <section class="section">
    <div class="container has-text-centered">
      <h1 class="title">About Djacket</h1>
      <p class="subtitle">
        This is a demo e-commerce site built with Django and Vue.js.
      </p>
    </div>
  </section>
</template>

<script>
export default {
  name: 'About',
  mounted() {
    document.title = 'About | Djackets'
  },
}
</script>

<style scoped>
/* optional styles */
</style>

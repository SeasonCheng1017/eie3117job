<template>
  <div class="home">
    <section class="hero is-medium is-dark mb-6">
      <div class="hero-body has-text-centered">
        <p class="title mb-6">Welcome to JobHunt</p>
        <p class="subtitle">Find your dream job or hire top talent</p>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  mounted() {
    document.title = 'JobHunt - Home'
  }
}
</script>

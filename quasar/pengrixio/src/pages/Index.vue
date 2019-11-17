<template>
  <div></div>
</template>

<script>
export default {
  name: 'PageIndex',
  data () {
    return {
    }
  },
  methods: {
    redirect: function () {
      if (this.$store.state.pengrixio.login) {
        this.$router.push('/edge/')
      } else {
        this.$router.push('/login/admin')
      }
    }
  },
  mounted () {
    this.redirect()
  }
}
</script>

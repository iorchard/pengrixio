<template>
  <div>
  </div>
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
        if (this.$store.state.pengrixio.role === 'admin') {
          this.$router.push('/dashboard/')
        } else {
          this.$router.push('/user/')
        }
      } else {
        this.$router.push('/login/')
      }
    }
  },
  mounted () {
    this.redirect()
  }
}
</script>

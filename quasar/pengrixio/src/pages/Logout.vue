<template>
  <div></div>
</template>

<script>
export default {
  name: 'Logout',
  data () {
    return {}
  },
  methods: {
    logout: function () {
      this.$store.commit('pengrixio/loggedIn', false)
      this.$store.commit('pengrixio/setName', '')
      this.$store.commit('pengrixio/setRole', '')
      this.$store.commit('pengrixio/setToken', '')
      this.$store.commit('pengrixio/setRefreshToken', '')
      this.$router.push('/login')
    }
  },
  mounted () {
    this.logout()
  }
}
</script>

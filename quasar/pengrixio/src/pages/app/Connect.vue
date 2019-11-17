<template>
  <q-page padding>
    <form action="http://192.168.24.6/guacamole/" target="_self"
      method="post" ref="form">
      <input name="username" v-model="username" type="hidden" />
      <input name="password" v-model="password" type="hidden" />
    </form>
  </q-page>
</template>

<script>
export default {
  name: 'appConnect',
  data () {
    return {
      username: 'jijisa',
      password: 'asdf1234'
    }
  },
  methods: {
    submit: function () {
      this.$refs.form.submit()
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }
    this.submit()
  }
}
</script>

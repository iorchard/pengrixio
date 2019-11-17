<template>
  <q-page padding>
    <div class="fit row justify-center items-center sm-gutter">
      <q-icon name="cloud" size="xl" color="blue" />
      <big>KT Edge Platform</big>
    </div>
    <div class="fit row justify-center">
      <q-input
        type="text"
        v-model="name"
        ref="name"
        stable-label="Admin ID"
        placeholder="Enter Admin ID."
      />
    </div>
    <div class="fit row justify-center">
      <q-input
        type="password"
        v-model="pass"
        v-on:keyup.enter="auth"
        stable-label="Admin Password"
        placeholder="Enter Admin Password."
      />
    </div>
    <div class="fit row justify-center">
      <q-btn
        icon="forward"
        @click="auth"
      >
        Login
      </q-btn>
    </div>
  </q-page>
</template>

<script>
import { API_URL } from '../config'
import axios from 'axios'
export default {
  name: 'Login',
  data () {
    return {
      name: '',
      pass: ''
    }
  },
  methods: {
    setAxiosHeaders: function (token) {
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
    },
    auth: function () {
      const url = API_URL + '/account/admin/login/'
      const dReqBody = {
        name: this.name,
        pass: this.pass
      }
      const headers = {
      }
      this.$axios.post(url, dReqBody, headers)
        .then((response) => {
          this.$store.commit('pengrixio/loggedIn', true)
          this.$store.commit('pengrixio/setName', this.name)
          this.$store.commit('pengrixio/setRole', response.data.role)
          this.$store.commit('pengrixio/setToken', response.data.token)
          this.$store.commit('pengrixio/setRefreshToken',
            response.data.refresh_token)
          this.setAxiosHeaders(response.data.token)
          this.$router.push('/edge/')
        })
        .catch(() => {
          console.log('Fail to login')
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Login failed.',
            icon: 'report_problem'
          })
        })
    }
  },
  mounted () {
    if (this.$store.state.pengrixio.login) {
      this.$router.push('/')
    }
    this.$refs.name.focus()
  }
}
</script>

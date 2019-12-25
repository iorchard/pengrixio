<template>
  <q-page padding>
    <div class="q-pa-md q-gutter-md">
      <div class="row justify-between">
        <q-parallax src="statics/login_bg.png" style="width:100%;" :height="800">
          <div>
            <q-icon name="cloud" size="xl" color="grey-4" />&nbsp;
            <big>KT Edge Platform</big>
          </div>
          <div>
            <big>VDI Service</big>
          </div>
          <div>
            <q-input
              type="text"
              v-model="name"
              ref="name"
              stable-label="ID"
              placeholder="Enter your ID."
            />
          </div>
          <div>
            <q-input
              type="password"
              v-model="pass"
              v-on:keyup.enter="auth"
              stable-label="Password"
              placeholder="Enter your password."
            />
          </div>
          <div>
            <q-btn
              icon="forward"
              @click="auth"
            >
              Login
            </q-btn>
          </div>
        </q-parallax>
      </div>
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
      const url = API_URL + '/account/login/'
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
          this.$router.push('/user/')
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

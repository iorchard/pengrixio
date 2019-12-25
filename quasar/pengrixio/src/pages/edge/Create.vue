<template>
  <q-page padding>
    <form>
      <div class="q-pa-md">

        <div class="q-gutter-md" style="max-width: 300px">
          <q-input v-model="form.name" label="Name" />
          <q-input v-model="form.endpoint" label="Endpoint" />
          <q-input v-model="form.broker" label="Broker" />
          <q-input v-model="form.broker_ip" label="Broker IP" />
          <q-input v-model="form.desc" label="Description" />
        </div>

        <div>
          <q-btn label="Register" color="primary" @click="submit" />
        </div>

      </div>
    </form>
  </q-page>
</template>

<script>
import { API_URL } from '../../config'

export default {
  name: 'accountCreate',
  data () {
    return {
      form: {
        name: '',
        endpoint: '',
        broker: '',
        broker_ip: '',
        desc: ''
      }
    }
  },
  methods: {
    submit: function () {
      if (!this.form.name) {
        this.$q.notify('Please enter User ID.')
        return
      }
      const payload = {
        name: this.form.name,
        endpoint: this.form.endpoint,
        broker: this.form.broker,
        broker_ip: this.form.broker_ip,
        desc: this.form.desc
      }
      const url = API_URL + '/edge/'
      this.$axios.post(url, payload)
        .then((response) => {
          this.$router.push('/edge/')
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Creating an edge is failed.',
            icon: 'report_problem'
          })
        })
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }
  }
}
</script>

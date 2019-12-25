<template>
  <q-page padding>
    <form>
      <div class="q-pa-md">

        <div class="q-gutter-md" style="max-width: 300px">
          <q-input v-model="form.name" label="Name" hint="read only" readonly />
          <q-input v-model="form.endpoint" label="Endpoint" />
          <q-input v-model="form.broker" label="Broker" />
          <q-input v-model="form.broker_ip" label="Broker IP" />
          <q-input v-model="form.desc" label="Description" />
        </div>

        <div>
          <q-btn label="Save" color="primary" @click="submit" />
        </div>

      </div>
    </form>
  </q-page>
</template>

<script>
import { API_URL } from '../../config'

export default {
  name: 'accountEdit',
  data () {
    return {
      form: {
        name: this.$route.params.name,
        endpoint: '',
        broker: '',
        broker_ip: '',
        desc: ''
      }
    }
  },
  methods: {
    submit: function () {
      const payload = {
        endpoint: this.form.endpoint,
        broker: this.form.broker,
        broker_ip: this.form.broker_ip,
        desc: this.form.desc
      }
      const url = API_URL + '/edge/' + this.$route.params.name + '/'
      this.$axios.patch(url, payload)
        .then((response) => {
          this.$router.push('/edge/')
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Updating an edge is failed.',
            icon: 'report_problem'
          })
        })
    },
    getEdgeInfo: function () {
      const url = API_URL + '/edge/' + this.$route.params.name + '/'
      this.$axios.get(url)
        .then((response) => {
          this.form = response.data
          console.log(this.form)
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Getting edge info failed.',
            icon: 'report_problem'
          })
        })
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }
    this.getEdgeInfo()
  }
}
</script>

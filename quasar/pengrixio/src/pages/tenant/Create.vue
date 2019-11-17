<template>
  <q-page padding>
    <form>
      <div class="q-pa-md">

        <div class="q-gutter-md" style="max-width: 300px">
          <q-input v-model="form.name" label="Name" />
          <q-input v-model="form.edge" label="Edge" />
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
      data: [],
      form: {
        name: '',
        edge: this.$route.params.edge_name,
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
        edge: this.form.edge,
        desc: this.form.desc
      }
      const url = API_URL + '/tenant/' + this.form.edge + '/'
      this.$axios.post(url, payload)
        .then((response) => {
          this.$router.push('/edge/' + this.form.edge + '/')
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Creating a tenant is failed.',
            icon: 'report_problem'
          })
        })
    },
    listTenants: function () {
      console.log(this.$route.params.edge_name)
      const url = API_URL + '/tenant/' + this.$route.params.edge_name + '/'
      this.$axios.get(url)
        .then((response) => {
          this.data = response.data
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Getting edge list failed.',
            icon: 'report_problem'
          })
        })
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }

    this.listTenants()
  }
}
</script>

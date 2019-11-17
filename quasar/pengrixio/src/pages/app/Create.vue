<template>
  <q-page padding>
    <form>
      <div class="q-pa-md">

        <div class="q-gutter-md" style="max-width: 300px">
          <q-input v-model="form.name" label="Name" hint="read only" readonly />
          <q-select v-model="form.catalog" :options="form.options"
            @input="fillInName"
            label="Catalog" />
          <q-input v-model="form.user" label="User" hint="read only" readonly />
          <q-input v-model="form.desc" label="Description" />
        </div>

        <div>
          <q-btn label="Create" color="primary" @click="submit" />
        </div>

      </div>
    </form>
  </q-page>
</template>

<script>
import { API_URL } from '../../config'

export default {
  name: 'appCreate',
  data () {
    return {
      data: [],
      form: {
        name: '',
        catalog: '',
        options: [],
        user: this.$route.params.user,
        desc: ''
      }
    }
  },
  methods: {
    fillInName: function () {
      console.log('haha' + this.form.catalog + 'hoho')
      if (this.form.catalog === '') {
        this.form.name = ''
      } else {
        this.form.name = this.form.user + '-' + this.form.catalog + '-' +
          Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 4)
      }
    },
    submit: function () {
      if (!this.form.name) {
        this.$q.notify('Please enter app name.')
        return
      }
      const payload = {
        name: this.form.name,
        catalog: this.form.catalog,
        user: this.form.user,
        desc: this.form.desc
      }
      console.log(payload)
      const url = API_URL + '/app/'
      this.$axios.post(url, payload)
        .then((response) => {
          this.$router.push('/account/')
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Creating an app is failed.',
            icon: 'report_problem'
          })
        })
    },
    getCatalogList: function () {
      const url = API_URL + '/catalog/'
      this.$axios.get(url)
        .then((response) => {
          this.form.options.push('')
          for (let i in response.data) {
            let r = response.data[i]
            this.form.options.push(r.name)
          }
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Getting catalog list is failed.',
            icon: 'report_problem'
          })
        })
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }
    this.getCatalogList()
  }
}
</script>

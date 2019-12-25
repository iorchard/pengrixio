<template>
  <q-page padding>
    <form>
      <div class="q-pa-md">

        <div class="q-gutter-md" style="max-width: 300px">
          <q-input v-model="form.name" label="Name" hint="read only" readonly />
          <q-select v-model="form.type" :options="typeOptions"
            hint="Type" />
          <q-input v-model="form.logo" label="Logo image name" />
          <q-badge color="secondary">CPU (ea)</q-badge>
          <q-slider v-model="form.cpu_spec" label label-always
           :min="1" :max="16" :step="1"
          />
          <q-badge color="secondary">Memory (GiB)</q-badge>
          <q-slider v-model="form.mem_spec" label label-always
           :min="1" :max="16" :step="1"
          />
          <q-badge color="secondary">Disk (GiB)</q-badge>
          <q-slider v-model="form.disk_spec" label label-always
           :min="10" :max="100" :step="10"
          />
          <q-input v-model="form.image_url" label="Image URL" />
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
  name: 'catalogEdit',
  data () {
    return {
      data: [],
      typeOptions: ['vm', 'container'],
      form: {
        name: this.$route.params.name,
        logo: '',
        type: 'vm',
        cpu_spec: 1,
        mem_spec: 1,
        disk_spec: 10,
        image_url: '',
        desc: ''
      }
    }
  },
  methods: {
    submit: function () {
      if (!this.form.name) {
        this.$q.notify('Please enter catalog name.')
        return
      }
      const payload = {
        name: this.form.name,
        logo: this.form.logo,
        type: this.form.type,
        cpu_spec: this.form.cpu_spec,
        mem_spec: this.form.mem_spec,
        disk_spec: this.form.disk_spec,
        image_url: this.form.image_url,
        desc: this.form.desc
      }
      console.log(payload)
      const url = API_URL + '/catalog/' + this.$route.params.name + '/'
      this.$axios.patch(url, payload)
        .then((response) => {
          this.$router.push('/catalog/')
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Updating a catalog is failed.',
            icon: 'report_problem'
          })
        })
    },
    getCatalogInfo: function () {
      const url = API_URL + '/catalog/' + this.$route.params.name + '/'
      this.$axios.get(url)
        .then((response) => {
          this.form = response.data
        })
        .catch((e) => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: e,
            icon: 'report_problem'
          })
        })
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }
    this.getCatalogInfo()
  }
}
</script>

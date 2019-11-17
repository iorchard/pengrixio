<template>
  <q-page padding>
    <div class="q-pa-md">

      <q-bar dark>
        <div class="row">
          <div>
            <q-btn color="primary" icon="add" size="md" rounded dense
              @click="projectCreate = true" label="Add"
            />
            <q-tooltip>Create a tenant</q-tooltip>
          </div>
          <div>
            <q-btn color="primary" icon="refresh" size="md" rounded dense
              @click="listProjects" label="Reload"
            />
            <q-tooltip>Reload</q-tooltip>
          </div>
        </div>
      </q-bar>

      <q-table
        title="Tenants"
        :data="data"
        :columns="columns"
        row-key="name"
        :filter="filter"
        :pagination.sync="pagination"
        :loading="loading"
      >

        <template v-slot:top-right>
          <q-input dense debounce="300" v-model="filter"
            place-holder="Search">
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </template>

        <template v-slot:body-cell-functions="props">
          <q-td :props="props">
            <div>
              <q-btn color="primary" icon="delete"
                size="sm" round dense
                @click="name=props.row.name; confirmDelete = true"
              >
                <q-tooltip>Delete a tenant</q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </template>

      </q-table>

      <q-dialog v-model="projectCreate">
        <q-card style="width:700px;max-width:80vw;">
          <q-card-section class="row items-center">
            <div class="text-h6">Create a tenant</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <form>
              <q-input rounded standout v-model="form.name"
                label="Enter a tenant name" />
              <q-btn flat color="white" text-color="black"
                label="Close" v-close-popup />
              <q-btn flat color="primary" label="Create" v-close-popup
                @click="submit" />
            </form>
          </q-card-section>
        </q-card>
      </q-dialog>

      <q-dialog v-model="confirmDelete">
        <q-card>
          <q-card-section class="row items-center">
            <q-avatar icon="delete" color="primary" text-color="white" />
            <span class="q-ml-sm">
              Are you sure to delete a tenant ({{ name }})?
            </span>
          </q-card-section>

          <q-card-section>
            <q-btn flat label="Cancel" color="primary" v-close-popup />
            <q-btn flat label="OK" color="primary" v-close-popup
              @click="processDelete(name)"
            />
          </q-card-section>
        </q-card>
      </q-dialog>

    </div>
  </q-page>
</template>

<script>
import { API_URL } from '../../config'
export default {
  name: 'ProjectList',
  data () {
    return {
      data: [],
      loading: false,
      projectCreate: false,
      confirmDelete: false,
      form: { name: '' },
      name: '',
      filter: '',
      pagination: {
        sortBy: 'name',
        descending: false,
        rowsPerPage: 10
      },
      columns: [
        { name: 'name', required: true, label: 'Name', field: 'name' },
        { name: 'pods', label: 'Pods', field: 'pods' },
        { name: 'status', label: 'Status', field: 'status' },
        { name: 'createdAt',
          label: 'Created',
          field: 'createdAt',
          format: (val) => { return val ? new Date(val).toLocaleString() : '' }
        },
        { name: 'functions', label: 'Functions', field: 'functions' }
      ]
    }
  },
  methods: {
    processDelete: function (name) {
      const url = API_URL + `/project/${name}`
      this.$axios.delete(url)
        .then((response) => {
          this.listProjects()
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Deleting a tenant is failed.',
            icon: 'report_problem'
          })
        })
    },
    submit: function () {
      let pattern = /[a-z0-9]([-a-z0-9]*[a-z0-9])?/
      if (!pattern.test(this.form.name)) {
        let err = 'Name should be alphanumeric and hypen only.'
        this.$q.notify({
          color: 'negative',
          position: 'top',
          message: err,
          icon: 'report_problem'
        })
      } else {
        const url = API_URL + '/project/'
        const payload = { name: this.form.name }
        console.log(payload)
        this.$axios.post(url, payload)
          .then((response) => {
            this.listProjects()
          })
          .catch(() => {
            this.$q.notify({
              color: 'negative',
              position: 'bottom',
              message: 'Creating a tenant is failed.',
              icon: 'report_problem'
            })
          })
      }
    },
    listProjects: function () {
      this.loading = true
      const url = API_URL + '/project/'
      this.$axios.get(url)
        .then((response) => {
          this.data = response.data
        })
        .catch(() => {
          this.$q.noticy({
            color: 'negative',
            position: 'top',
            message: 'Getting tenant list is failed.',
            icon: 'report_problem'
          })
        })
        .finally(() => {
          this.loading = false
        })
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }
    this.listProjects()
  }
}
</script>

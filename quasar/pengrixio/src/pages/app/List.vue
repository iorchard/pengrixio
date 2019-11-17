<template>
  <q-page padding>
    <div class="q-pa-md">

      <q-table
        title="Apps"
        :data="data"
        :columns="columns"
        row-key="name"
        :filter="filter"
        :pagination.sync="pagination"
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
              <q-btn color="primary" icon="info"
                size="sm" round dense
                @click="getAppInfo(props.row.name); appInfo = true"
              >
                <q-tooltip>View an app.</q-tooltip>
              </q-btn>
              <q-btn color="primary" icon="delete"
                size="sm" round dense
                @click="getAppInfo(props.row.name); confirmDelete = true"
              >
                <q-tooltip>Delete an app.</q-tooltip>
              </q-btn>
              <q-btn color="primary" icon="computer"
                size="sm" round dense
                @click="goToConnect(props.row.name)"
              >
                <q-tooltip>Connect to an app.</q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </template>

      </q-table>

      <q-dialog v-model="appInfo">
        <q-card>
          <q-card-section class="row items-center">
            <div class="text-h6">App Info</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            name: {{ app.name }}
          </q-card-section>
        </q-card>
      </q-dialog>

      <q-dialog v-model="confirmDelete">
        <q-card>
          <q-card-section class="row items-center">
            <q-avatar icon="delete" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure to delete an app ?</span>
          </q-card-section>

          <q-card-section>
            <q-btn flat label="Cancel" color="primary" v-close-popup />
            <q-btn flat label="OK" color="primary" v-close-popup
              @click="processDelete(app.name)"
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
  name: 'AppList',
  data () {
    return {
      data: [],
      app: {},
      appInfo: false,
      confirmDelete: false,
      filter: '',
      pagination: {
        sortBy: 'name',
        descending: false,
        rowsPerPage: 10
      },
      columns: [
        { name: 'name', required: true, label: 'Name', field: 'name' },
        { name: 'catalog', label: 'Catalog', field: 'catalog' },
        { name: 'tenant', label: 'Tenant', field: 'tenant' },
        { name: 'user', label: 'User', field: 'user' },
        { name: 'description', label: 'Description', field: 'desc' },
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
    goToConnect: function (name) {
      window.open('http://192.168.24.6/guacamole/')
    },
    processDelete: function (name) {
      const url = API_URL + `/app/${name}/`
      this.$axios.delete(url)
        .then((response) => {
          this.$q.notify({
            color: 'primary',
            position: 'bottom',
            message: 'Deleting an app is succeeded.',
            icon: 'thumb_up'
          })
          this.listApps()
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Deleting an app is failed.',
            icon: 'report_problem'
          })
        })
    },
    getAppInfo: function (name) {
      const url = API_URL + `/app/${name}/`
      this.$axios.get(url)
        .then((response) => {
          this.app = response.data
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Getting app info failed.',
            icon: 'report_problem'
          })
        })
    },
    listApps: function () {
      const url = API_URL + '/app/'
      this.$axios.get(url)
        .then((response) => {
          this.data = response.data
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Getting app list failed.',
            icon: 'report_problem'
          })
        })
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }
    this.listApps()
  }
}
</script>

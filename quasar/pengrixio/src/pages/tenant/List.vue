<template>
  <q-page padding>
    <div class="q-pa-md">

      <q-table
        title="Tenants"
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
                @click="getTenantInfo(props.row.name); tenantInfo = true"
              >
                <q-tooltip>View a tenant</q-tooltip>
              </q-btn>
              <q-btn color="primary" icon="delete"
                size="sm" round dense
                @click="getTenantInfo(props.row.name); confirmDelete = true"
              >
                <q-tooltip>Delete a tenant.</q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </template>

      </q-table>

      <q-dialog v-model="tenantInfo">
        <q-card>
          <q-card-section class="row items-center">
            <div class="text-h6">Tenant Info</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            name: {{ tenant.name }}
          </q-card-section>
        </q-card>
      </q-dialog>

      <q-dialog v-model="confirmDelete">
        <q-card>
          <q-card-section class="row items-center">
            <q-avatar icon="delete" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure to delete a tenant ?</span>
          </q-card-section>

          <q-card-section>
            <q-btn flat label="Cancel" color="primary" v-close-popup />
            <q-btn flat label="OK" color="primary" v-close-popup
              @click="processDelete(tenant.name)"
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
  name: 'TenantList',
  data () {
    return {
      data: [],
      tenant: {},
      tenantInfo: false,
      confirmDelete: false,
      filter: '',
      pagination: {
        sortBy: 'name',
        descending: false,
        rowsPerPage: 10
      },
      columns: [
        { name: 'name', required: true, label: 'Name', field: 'name' },
        { name: 'edge', label: 'Edge', field: 'edge' },
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
    processDelete: function (name) {
      const url = API_URL + `/tenant/${name}/`
      this.$axios.delete(url)
        .then((response) => {
          this.$q.notify({
            color: 'primary',
            position: 'bottom',
            message: 'Deleting a tenant is succeeded.',
            icon: 'thumb_up'
          })
          this.listApps()
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
    getTenantInfo: function (name) {
      const url = API_URL + `/tenant/${name}/`
      this.$axios.get(url)
        .then((response) => {
          this.app = response.data
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Getting tenant info failed.',
            icon: 'report_problem'
          })
        })
    },
    listTenants: function () {
      const url = API_URL + '/tenant/'
      this.$axios.get(url)
        .then((response) => {
          this.data = response.data
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Getting tenant list failed.',
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

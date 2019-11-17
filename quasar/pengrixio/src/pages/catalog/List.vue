<template>
  <q-page padding>
    <div class="q-pa-md">
      <q-bar>
        <div>
          <q-btn color="primary" icon="add" size="md" rounded dense
            @click="goToCreate" label="Add"
          />
          <q-tooltip>Create a catalog</q-tooltip>
        </div>
      </q-bar>

      <q-table
        title="Catalogs"
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
                @click="getCatalogInfo(props.row.name); catalogInfo = true"
              >
                <q-tooltip>View a catalog</q-tooltip>
              </q-btn>
              <q-btn color="primary" icon="delete"
                size="sm" round dense
                @click="getCatalogInfo(props.row.name); confirmDelete = true"
              >
                <q-tooltip>Delete a catalog</q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </template>

      </q-table>

      <q-dialog v-model="catalogInfo">
        <q-card>
          <q-card-section class="row items-center">
            <div class="text-h6">Catalog Info</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            name: {{ catalog.name }}
          </q-card-section>
        </q-card>
      </q-dialog>

      <q-dialog v-model="confirmDelete">
        <q-card>
          <q-card-section class="row items-center">
            <q-avatar icon="delete" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure to delete a catalog?</span>
          </q-card-section>

          <q-card-section>
            <q-btn flat label="Cancel" color="primary" v-close-popup />
            <q-btn flat label="OK" color="primary" v-close-popup
              @click="processDelete(catalog.name)"
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
  name: 'CatalogList',
  data () {
    return {
      data: [],
      catalog: {},
      catalogInfo: false,
      confirmDelete: false,
      filter: '',
      pagination: {
        sortBy: 'name',
        descending: false,
        rowsPerPage: 10
      },
      columns: [
        { name: 'name', required: true, label: 'User ID', field: 'name' },
        { name: 'cpu', label: 'CPU(ea)', field: 'cpu_spec' },
        { name: 'memory', label: 'Memory(GiB)', field: 'mem_spec' },
        { name: 'disk', label: 'Disk(GiB)', field: 'disk_spec' },
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
      const url = API_URL + `/catalog/${name}/`
      this.$axios.delete(url)
        .then((response) => {
          this.$q.notify({
            color: 'primary',
            position: 'bottom',
            message: 'Deleting a catalog is succeeded.',
            icon: 'thumb_up'
          })
          this.listCatalogs()
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Deleting a catalog is failed.',
            icon: 'report_problem'
          })
        })
    },
    goToCreate: function () {
      this.$router.push('/catalog/create/')
    },
    getCatalogInfo: function (name) {
      const url = API_URL + `/catalog/${name}/`
      this.$axios.get(url)
        .then((response) => {
          this.catalog = response.data
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Getting catalog info failed.',
            icon: 'report_problem'
          })
        })
    },
    listCatalogs: function () {
      const url = API_URL + '/catalog/'
      this.$axios.get(url)
        .then((response) => {
          this.data = response.data
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Getting catalog list failed.',
            icon: 'report_problem'
          })
        })
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }
    this.listCatalogs()
  }
}
</script>

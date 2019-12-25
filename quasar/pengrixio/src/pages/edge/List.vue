<template>
  <q-page padding>
    <div>
      <q-btn color="primary" icon="add"
        rounded
        @click="goToCreate"
        label="Add"
      >
        <q-tooltip
          content-class="bg-purple" content-style="font-size: 16px"
        >Create an edge.</q-tooltip>
      </q-btn>
    </div>
    <div class="q-pa-sm">

      <q-table
        title="Edges"
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
                @click="getEdgeInfo(props.row.name); edgeInfo = true"
              >
                <q-tooltip
                  content-class="bg-purple" content-style="font-size: 16px"
                >View an edge</q-tooltip>
              </q-btn>
              <q-btn color="primary" icon="edit"
                size="sm" round dense
                @click="goToEdit(props.row.name)"
              >
                <q-tooltip
                  content-class="bg-purple" content-style="font-size: 16px"
                >Update an edge.</q-tooltip>
              </q-btn>
              <q-btn color="primary" icon="delete"
                size="sm" round dense
                @click="getEdgeInfo(props.row.name); confirmDelete = true"
              >
                <q-tooltip
                  content-class="bg-purple" content-style="font-size: 16px"
                >Delete an edge.</q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </template>

      </q-table>

      <q-dialog v-model="edgeInfo">
        <q-card>
          <q-card-section class="row items-center">
            <div class="text-h6">Edge Info</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            name: {{ edge.name }}
          </q-card-section>
        </q-card>
      </q-dialog>

      <q-dialog v-model="confirmDelete">
        <q-card>
          <q-card-section class="row items-center">
            <q-avatar icon="delete" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure to delete an edge?</span>
          </q-card-section>

          <q-card-section>
            <q-btn flat label="Cancel" color="primary" v-close-popup />
            <q-btn flat label="OK" color="primary" v-close-popup
              @click="processDelete(edge.name)"
            />
          </q-card-section>
        </q-card>
      </q-dialog>

    </div>
  </q-page>
</template>

<script>
import { API_URL, POLLING_INTERVAL } from '../../config'
export default {
  name: 'EdgeList',
  data () {
    return {
      edge: {},
      confirmDelete: false,
      edgeInfo: false,
      filter: '',
      data: [],
      pagination: {
        sortBy: 'name',
        descending: false,
        rowsPerPage: 10
      },
      columns: [
        { name: 'name', required: true, label: 'Name', field: 'name' },
        { name: 'endpoint', label: 'Endpoint', field: 'endpoint' },
        { name: 'broker', label: 'Broker', field: 'broker' },
        { name: 'desc', label: 'Description', field: 'desc' },
        { name: 'createdAt',
          label: 'Created',
          field: 'createdAt',
          format: (val) => { return val ? new Date(val).toLocaleString() : '' }
        },
        { name: 'modifiedAt',
          label: 'Modified',
          field: 'modifiedAt',
          format: (val) => { return val ? new Date(val).toLocaleString() : '' }
        },
        { name: 'functions', label: 'Functions', field: 'functions' }
      ]
    }
  },
  methods: {
    processDelete: function (name) {
      const url = API_URL + `/edge/${name}/`
      this.$axios.delete(url)
        .then((response) => {
          this.$q.notify({
            color: 'primary',
            position: 'top',
            message: 'Deleting an edge is succeeded.',
            icon: 'thumb_up'
          })
          this.$router.push('/edge/')
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Deleting an edge is failed.',
            icon: 'report_problem'
          })
        })
    },
    goToCreate: function () {
      this.$router.push('/edge/create/')
    },
    goToEdge: function (name) {
      this.$router.push(`/edge/${name}/`)
    },
    goToEdit: function (name) {
      this.$router.push(`/edge/${name}/edit/`)
    },
    getEdgeInfo: function (name) {
      const url = API_URL + `/edge/${name}/`
      this.$axios.get(url)
        .then((response) => {
          this.edge = response.data
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Getting edge info failed.',
            icon: 'report_problem'
          })
        })
    },
    getEdges: function () {
      const url = API_URL + '/edge/'
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
    this.getEdges()
    this.intervalObj = setInterval(this.getEdges, POLLING_INTERVAL)
  },
  destroyed: function () {
    clearInterval(this.intervalObj)
  }
}
</script>
<style lang="stylus">
.edge-card
  width 97%
</style>

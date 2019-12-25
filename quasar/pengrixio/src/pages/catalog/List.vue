<template>
  <q-page padding>
    <div class="q-pa-md">
      <q-bar>
        <div>
          <q-btn color="primary" icon="add" size="md" rounded dense
            @click="goToCreate" label="Add"
          />
          <q-tooltip
            content-class="bg-purple" content-style="font-size: 16px"
          >Create a catalog</q-tooltip>
        </div>
      </q-bar>

      <q-table
        title="App Hub"
        grid
        :data="data"
        :columns="columns"
        row-key="name"
        :filter="filter"
        :pagination.sync="pagination"
        no-data-label="There is no data."
      >

        <template v-slot:top-right>
          <q-input dense debounce="300" v-model="filter"
            place-holder="Search">
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </template>

        <template v-slot:item="props">
          <!--<div class="q-pa-md col-xs-12 col-sm-6 col-md-4 col-lg-3">-->
          <div class="q-pa-md">
            <q-card>
              <q-img :src="'statics/' + props.row.logo" basic
                style="height: 120px;">
                <div class="absolute-top">
                  <span class="text-h6">{{ props.row.name }}</span>&nbsp;
                  <q-btn size="md" round dense color="primary" icon="edit"
                    @click="goToEdit(props.row.name)">
                    <q-tooltip content-class="bg-purple"
                      content-style="font-size: 16px">
                      Edit
                    </q-tooltip>
                  </q-btn>
                  &nbsp;
                  <q-btn size="md" round dense color="negative" icon="delete"
                  @click="getCatalogInfo(props.row.name); confirmDelete = true"
                  >
                    <q-tooltip content-class="bg-purple"
                      content-style="font-size: 16px">
                      Delete
                    </q-tooltip>
                  </q-btn>
                </div>
              </q-img>
              <q-separator />
              <q-list dense>
                <q-item
                  v-for="col in props.cols.filter(col => col.name !== 'name')"
                  :key="col.name">
                  <q-item-section>
                    <q-item-label>{{ col.label }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-item-label caption v-if="col.name === 'type'">
                      <q-badge class="text-h6" color="primary"
                        :label="col.value" />
                    </q-item-label>
                    <q-item-label caption v-else>
                      {{ col.value }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-card>
          </div>
        </template>
      </q-table>

      <q-dialog v-model="confirmDelete">
        <q-card>
          <q-card-section class="row items-center">
            <q-avatar icon="delete" color="primary" text-color="white" />
            <span class="q-ml-sm">
              Are you sure to delete a catalog {{ catalog.name }}?
            </span>
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
        { name: 'name', required: true, label: 'Name', field: 'name' },
        { name: 'type', label: 'Type', field: 'type' },
        { name: 'cpu', label: 'CPU(ea)', field: 'cpu_spec' },
        { name: 'memory', label: 'Memory(GiB)', field: 'mem_spec' },
        { name: 'disk', label: 'Disk(GiB)', field: 'disk_spec' },
        { name: 'description', label: 'Description', field: 'desc' },
        { name: 'createdAt',
          label: 'Created',
          field: 'createdAt',
          format: (val) => { return val ? new Date(val).toLocaleString() : '' }
        }
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
    goToEdit: function (name) {
      this.$router.push(`/catalog/${name}/edit`)
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

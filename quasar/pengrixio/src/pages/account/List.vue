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
          >Create an account</q-tooltip>
        </div>
      </q-bar>

      <q-table
        title="Accounts"
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

        <template v-slot:body-cell-name="props">
          <q-td :props="props">
            <div v-if="props.value === 'admin'">
              <q-badge color="purple" :label="props.value" />
            </div>
            <div v-else>
              {{ props.value }}
            </div>
          </q-td>
        </template>
        <template v-slot:body-cell-functions="props">
          <q-td :props="props">
            <div>
              <q-btn color="primary" icon="info"
                size="sm" round dense
                @click="getUserInfo(props.row.name); userInfo = true"
              >
                <q-tooltip
                  content-class="bg-purple" content-style="font-size: 16px"
                >View an account</q-tooltip>
              </q-btn>
              <q-btn color="primary" icon="apps"
                size="sm" round dense
                @click="goToCreateApp(props.row.name)"
              >
                <q-tooltip
                  content-class="bg-purple" content-style="font-size: 16px"
                >Create an app</q-tooltip>
              </q-btn>
              <q-btn color="primary" icon="delete"
                size="sm" round dense
                @click="getUserInfo(props.row.name); confirmDelete = true"
              >
                <q-tooltip
                  content-class="bg-purple" content-style="font-size: 16px"
                >Delete an account</q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </template>

      </q-table>

      <q-dialog v-model="userInfo">
        <q-card>
          <q-card-section class="row items-center">
            <div class="text-h6">User Info</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            name: {{ user.name }}
          </q-card-section>
        </q-card>
      </q-dialog>

      <q-dialog v-model="confirmDelete">
        <q-card>
          <q-card-section class="row items-center">
            <q-avatar icon="delete" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure to delete a user?</span>
          </q-card-section>

          <q-card-section>
            <q-btn flat label="Cancel" color="primary" v-close-popup />
            <q-btn flat label="OK" color="primary" v-close-popup
              @click="processDelete(user.name)"
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
  name: 'AccountList',
  data () {
    return {
      data: [],
      user: {},
      userInfo: false,
      confirmDelete: false,
      filter: '',
      pagination: {
        sortBy: 'name',
        descending: false,
        rowsPerPage: 10
      },
      columns: [
        { name: 'name', sortable: true, required: true, label: 'User ID', field: 'name' },
        { name: 'cn', sortable: true, label: 'Name', field: 'cn' },
        { name: 'tenant', sortable: true, label: 'Tenant', field: 'tenant' },
        { name: 'role', label: 'Role', field: 'role' },
        { name: 'state', sortable: true, label: 'State', field: 'state' },
        { name: 'expireAt',
          sortable: true,
          label: 'Expire Date',
          field: 'expireAt',
          format: (val) => { return val ? new Date(val).toLocaleString() : '' }
        },
        { name: 'createdAt',
          label: 'Creation Date',
          field: 'createdAt',
          format: (val) => { return val ? new Date(val).toLocaleString() : '' }
        },
        { name: 'functions', label: 'Functions', field: 'functions' }
      ]
    }
  },
  methods: {
    processDelete: function (name) {
      const url = API_URL + `/account/${name}/`
      this.$axios.delete(url)
        .then((response) => {
          this.$q.notify({
            color: 'primary',
            position: 'bottom',
            message: 'Deleting an account is succeeded.',
            icon: 'thumb_up'
          })
          this.listAccounts()
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Deleting an account is failed.',
            icon: 'report_problem'
          })
        })
    },
    goToCreateApp: function (user) {
      this.$router.push(`/app/create/${user}/`)
    },
    goToCreate: function () {
      this.$router.push('/account/create/')
    },
    getUserInfo: function (name) {
      console.log(name)
      const url = API_URL + `/account/${name}/`
      this.$axios.get(url)
        .then((response) => {
          this.user = response.data
          console.log(this.user)
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Getting account info failed.',
            icon: 'report_problem'
          })
        })
    },
    listAccounts: function () {
      const url = API_URL + '/account/'
      this.$axios.get(url)
        .then((response) => {
          this.data = response.data
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Getting account list failed.',
            icon: 'report_problem'
          })
        })
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }
    this.listAccounts()
  }
}
</script>

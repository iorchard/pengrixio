<template>
  <q-page padding>
    <div class="q-pa-sm">

      <q-splitter
        v-model="splitterModel"
      >

        <template v-slot:before>
          <div class="q-pa-sm">
            <div class="text-h4 q-mb-sm">
              <q-icon name="device_hub" size="xl" style="color:#ccc" />
              {{ edge.name }}
            </div>
            <div class="text-subtitle2">{{ edge.desc }}</div>
            <div>
              <q-list bordered dense>
                <q-item>
                  <q-item-section>Status</q-item-section>
                  <q-item-section style="color:#0000ff">
                    <q-badge :color="statusColor">{{ edge.status }}</q-badge>
                  </q-item-section>
                </q-item>
                <q-item>
                  <q-item-section>CPU</q-item-section>
                  <q-item-section style="color:#0000ff">
                    {{ edge.cpu }} cores
                  </q-item-section>
                </q-item>
                <q-item>
                  <q-item-section>Memory</q-item-section>
                  <q-item-section style="color:#0000ff">
                    {{ edge.memory }} GiB
                  </q-item-section>
                </q-item>
                <q-item>
                  <q-item-section>Storage</q-item-section>
                  <q-item-section style="color:#0000ff">
                    {{ edge.used_stor }}/{{ edge.tot_stor }} GiB
                  </q-item-section>
                </q-item>
                <q-item>
                  <q-item-section>Hosts/Tenants/Apps</q-item-section>
                  <q-item-section style="color:#0000ff">
                    {{ edge.hosts }}/1/1
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
          </div>
        </template>

        <template v-slot:after>

          <div class="q-pa-sm">
            <div class="text-h6 q-mb-md">
              <q-icon name="business" size="lg" style="color:#ccc" />
              Tenants
            </div>
          </div>
          <q-bar dark>
            <div>
              <q-btn color="primary" icon="add" size="md" rounded dense
                @click="goToCreate" label="New"
              />
              <q-tooltip>Create a tenant</q-tooltip>
            </div>
          </q-bar>
          <div v-for="t in data" :key="t.name" class="row">
            <q-card class="tenant-card">
              <q-card-section>
                <div class="text-h6">{{ t.name }}</div>
                <div class="text-subtitle2">{{ t.desc }}</div>
              </q-card-section>
              <q-separator />
              <q-card-section>
                <div class="row">
                  <div>
                    <q-card v-for="a in t.app" :key="a.name">
                      <q-img src="statics/win10-logo-256x256.png" basic>
                        <div class="absolute-top">{{ a.name }}</div>
                      </q-img>
                      <q-card-section>
                         <div>사용자: {{ a.user }}</div>
                      </q-card-section>
                      <q-card-section>
                         <div>설명: {{ a.desc }}</div>
                      </q-card-section>
                      <q-card-actions>
                        <q-btn icon="play_arrow"
                          flat round color="primary"
                        >
                          <q-tooltip>Run</q-tooltip>
                        </q-btn>
                        <q-btn icon="stop"
                          flat round color="primary"
                        >
                          <q-tooltip>Stop</q-tooltip>
                        </q-btn>
                        <q-btn icon="call_made"
                          flat round color="primary"
                        >
                          <q-tooltip>Connect</q-tooltip>
                        </q-btn>
                        <q-btn icon="delete"
                          flat round color="red"
                        >
                          <q-tooltip>Delete</q-tooltip>
                        </q-btn>
                      </q-card-actions>
                    </q-card>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </template>
      </q-splitter>
    </div>
  </q-page>
</template>

<script>
import { API_URL } from '../../config'
export default {
  name: 'EdgeList',
  data () {
    return {
      splitterModel: 25,
      edgeName: this.$route.params.name,
      statusColor: 'green',
      edge: {},
      data: []
    }
  },
  methods: {
    tenantDelete: function (name) {
      const url = API_URL + `/tenant/${name}/`
      this.$axios.delete(url)
        .then((response) => {
          this.$q.notify({
            color: 'primary',
            position: 'top',
            message: 'Deleting a tenant is succeeded.',
            icon: 'thumb_up'
          })
          this.$router.push(`/edge/${this.edgeName}/`)
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Deleting a tenant is failed.',
            icon: 'report_problem'
          })
        })
    },
    goToCreate: function () {
      this.$router.push(`/tenant/create/${this.edgeName}/`)
    },
    getEdgeInfo: function () {
      const url = API_URL + '/edge/' + this.$route.params.name + '/'
      this.$axios.get(url)
        .then((response) => {
          this.edge = response.data
          console.log(this.user)
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
    listTenants: function () {
      const url = API_URL + `/tenant/${this.edgeName}/`
      this.$axios.get(url)
        .then((response) => {
          for (let i in response.data) {
            let r = response.data[i]
            console.log(r.app[0].name)
          }
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
    this.getEdgeInfo()
    this.listTenants()
  }
}
</script>
<style lang="stylus">
.tenant-card
  width 100%
</style>

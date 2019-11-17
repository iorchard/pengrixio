<template>
  <q-page padding>
    <div class="q-pa-sm">

      <q-splitter
        v-model="splitterModel"
      >

        <template v-slot:before>
          <div class="q-pa-sm">
            <div class="text-h5 q-mb-sm">
              <q-icon name="cloud" size="xl" style="color:#ccc" />
              Core Cloud
            </div>
            <div class="text-subtitle2">서초 KIDC</div>
            <div>
              <q-list bordered dense>
                <q-item>
                  <q-item-section>Status</q-item-section>
                  <q-badge :color="statusColor">Healthy</q-badge>
                </q-item>
                <q-item>
                  <q-item-section>Storage</q-item-section>
                  <q-item-section style="color:#0000ff">
                    {{ data[0].used_stor }} /
                    {{ data[0].tot_stor }} GiB ({{ data[0].storage }} %)
                  </q-item-section>
                </q-item>
                <q-item>
                  <q-item-section>Edges</q-item-section>
                  <q-item-section style="color:#0000ff">
                    2
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
          </div>
        </template>

        <template v-slot:after>

          <div class="q-pa-sm">
            <div class="text-h6 q-mb-md">
              <q-icon name="device_hub" size="lg" style="color:#ccc" />
              Edge Platform
            </div>
          </div>
          <q-bar dark>
            <div>
              <q-btn color="primary" icon="add" size="md" rounded dense
                @click="goToCreate" label="New"
              />
              <q-tooltip>Register an edge</q-tooltip>
            </div>
          </q-bar>
          <div v-for="e in data" :key="e.name" class="row">
            <q-card class="edge-card">
              <q-card-section>
                <div class="text-h6">{{ e.name ? e.name : '' }}</div>
                <div class="text-subtitle2">{{ e.desc ? e.desc : '' }}</div>
              </q-card-section>
              <q-separator />
              <q-card-section>
                <div class="row">
                  <div style="width:200px">
                    <apexchart type="radialBar"
                      :options="cpuOptions"
                      :series="[e.cpu]" />
                  </div>
                  <div style="width:200px">
                    <apexchart type="radialBar"
                      :options="memoryOptions"
                      :series="[e.memory]" />
                  </div>
                  <div style="width:200px">
                    <apexchart type="radialBar"
                      :options="storageOptions"
                      :series="[e.storage]" />
                  </div>
                  <div style="width:300px">

                    <q-list dense>
                      <q-item>
                        <q-item-section>Status</q-item-section>
                        <q-item-section style="color:#0000ff">
                          <q-badge :color="statusColor">{{ e.status }}</q-badge>
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section>CPU</q-item-section>
                        <q-item-section style="color:#0000ff">
                          {{ e.tot_cpu }} cores
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section>Memory</q-item-section>
                        <q-item-section style="color:#0000ff">
                          {{ e.tot_mem }} GiB
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section>Storage</q-item-section>
                        <q-item-section style="color:#0000ff">
                          {{ e.used_stor }}/{{ e.tot_stor }} GiB
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section>Hosts/Tenants/Apps</q-item-section>
                        <q-item-section style="color:#0000ff">
                          {{ e.hosts }}/{{ e.tenants }}/{{ e.apps }}
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </div>
                </div>
              </q-card-section>
              <q-separator />
              <q-card-actions>
                <q-btn icon="info" @click="goToEdge(e.name)" />
                <q-btn icon="delete" />
              </q-card-actions>
            </q-card>
          </div>
        </template>
      </q-splitter>
    </div>
  </q-page>
</template>

<script>
import { API_URL, POLLING_INTERVAL } from '../../config'
export default {
  name: 'EdgeList',
  data () {
    return {
      splitterModel: 20,
      edge: {},
      core: 0,
      data: [
        { name: '',
          desc: '',
          cpu: 0,
          memory: 0,
          storage: 0,
          status: '',
          tot_cpu: 0,
          tot_mem: 0,
          used_stor: 0,
          tot_str: 0,
          hosts: 0
        }
      ],
      statusColor: 'green',
      cpu: [],
      cpuOptions: {
        chart: {
          toolbar: { show: false }
        },
        stroke: {
          lineCap: 'round'
        },
        labels: ['CPU']
      },
      memory: [],
      memoryOptions: {
        chart: {
          toolbar: { show: false }
        },
        stroke: {
          lineCap: 'round'
        },
        labels: ['Memory']
      },
      storage: [],
      storageOptions: {
        chart: {
          toolbar: { show: false }
        },
        stroke: {
          lineCap: 'round'
        },
        labels: ['Storage']
      }
    }
  },
  methods: {
    showLoading () {
      this.$q.loading.show()
      this.timer = setTimeout(() => {
        this.$q.loading.hide()
        this.timer = void 0
      }, 5000)
    },
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
    listEdges: function () {
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
    this.showLoading()
    this.listEdges()
    this.intervalObj = setInterval(this.listEdges, POLLING_INTERVAL)
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

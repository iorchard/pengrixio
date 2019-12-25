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
                    {{ edge.cpu }} %
                  </q-item-section>
                </q-item>
                <q-item>
                  <q-item-section>Memory</q-item-section>
                  <q-item-section style="color:#0000ff">
                    {{ edge.memory }} %
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
                    {{ edge.hosts }}/{{ edge.tenants }}/{{ edge.apps }}
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

            <q-bar class="bg-white">
              <div>
                <q-btn color="primary" icon="add" size="md" rounded dense
                  @click="goToCreate" label="New"
                />
                <q-tooltip
                  content-class="bg-purple" content-style="font-size: 16px"
                >Create a tenant</q-tooltip>
              </div>
            </q-bar>
          </div>

          <div v-for="t in data" :key="t.name" class="row">
            <q-card class="tenant-card">
              <q-card-section class="bg-blue-grey-3">
                <div class="text-h6">{{ t.name }}</div>
                <div class="text-subtitle2">{{ t.desc }}</div>
              </q-card-section>
              <q-separator />
              <q-card-section>
                <div
                  class="fit row wrap justify-start content-start q-gutter-lg">
                  <q-card bordered v-for="a in t.app" :key="a.name">
                    <q-img :src="'statics/' + a.logo" basic>
                      <div class="absolute-top">{{ a.name }}</div>
                    </q-img>
                    <q-card-section>
                      <div>사용자: {{ a.user }}</div>
                      <div>상태:
                        <span v-if="a.status === 'running'">
                          <q-chip small icon="loop" text-color="white"
                            color="primary">
                            {{ a.status }}
                           </q-chip>
                         </span>
                         <span v-else-if="a.status.startsWith('building')">
                          <q-chip small icon="build" text-color="black"
                            color="warning">
                            {{ a.status }}
                           </q-chip>
                         </span>
                         <span v-else>
                          <q-chip small icon="stop" text-color="white"
                            color="negative">
                            {{ a.status }}
                           </q-chip>
                         </span>
                       </div>
                    </q-card-section>
                    <q-separator />
                    <q-card-actions align="around">
                      <q-btn icon="play_arrow" v-if="a.type == 'vm'"
                        flat round color="primary"
                        @click="runApp(a.name, a.status)"
                      >
                        <q-tooltip
                          content-class="bg-purple" content-style="font-size: 16px"
                        >Run</q-tooltip>
                      </q-btn>
                      <q-btn icon="stop" v-if="a.type == 'vm'"
                        flat round color="primary"
                        @click="stopApp(a.name, a.status)"
                      >
                        <q-tooltip
                          content-class="bg-purple" content-style="font-size: 16px"
                        >Stop</q-tooltip>
                      </q-btn>
                      <q-btn icon="call_made"
                        flat round color="primary"
                        @click="goToConnect(a.name, a.status)"
                      >
                        <q-tooltip
                          content-class="bg-purple" content-style="font-size: 16px"
                        >Connect</q-tooltip>
                      </q-btn>
                    </q-card-actions>
                  </q-card>
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
import { API_URL, POLLING_INTERVAL } from '../../config'
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
    runApp: function (name, status) {
      if (status === 'running') {
        this.$q.notify({
          color: 'warning',
          position: 'bottom',
          message: name + ' is already running.',
          icon: 'report_problem'
        })
        return
      }
      const url = API_URL + '/app/' + name + '/start/'
      this.$axios.post(url, {})
        .then((response) => {
          this.getTenants()
          this.$q.notify({
            color: 'primary',
            position: 'bottom',
            message: 'Succeed to start the app ' + name,
            icon: 'report_problem'
          })
        })
        .catch((error) => {
          console.log(error)
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Fail to start the app ' + name,
            icon: 'report_problem'
          })
        })
    },
    stopApp: function (name, status) {
      if (status === 'stopped') {
        this.$q.notify({
          color: 'warning',
          position: 'bottom',
          message: name + ' is already stopped.',
          icon: 'report_problem'
        })
        return
      }
      const url = API_URL + '/app/' + name + '/stop/'
      this.$axios.post(url, {})
        .then((response) => {
          console.log(response)
          this.getTenants()
          this.$q.notify({
            color: 'primary',
            position: 'bottom',
            message: 'Succeed to stop the app ' + name,
            icon: 'report_problem'
          })
        })
        .catch((error) => {
          console.log(error)
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Fail to stop the app ' + name + ':' + error,
            icon: 'report_problem'
          })
        })
    },
    goToConnect: function (name, status) {
      if (status !== 'running') {
        this.$q.notify({
          color: 'warning',
          position: 'bottom',
          message: name + ' is not running.',
          icon: 'report_problem'
        })
        return
      }
      // this.$router.push(`/app/connect/${name}/`)
      const url = API_URL + '/app/' + name + '/connect/'
      this.$axios.get(url)
        .then((response) => {
          this.broker = response.data
          // AppFullscreen.request()
          // let id = btoa(unescape(encodeURIComponent(name + 'noauth')))
          window.open('http://' + this.broker, name, 'height=' + screen.height + ',width=' + screen.width + ',fullcreen=yes')
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
    goToCreate: function () {
      this.$router.push(`/tenant/create/${this.edgeName}/`)
    },
    getEdgeInfo: function () {
      const url = API_URL + '/edge/' + this.$route.params.name + '/'
      this.$axios.get(url)
        .then((response) => {
          this.edge = response.data
          // console.log(this.edge.name)
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
    getTenants: function () {
      const url = API_URL + `/tenant/${this.edgeName}/`
      this.$axios.get(url)
        .then((response) => {
          for (let i in response.data) {
            let r = response.data[i]
            console.log(r['app'])
          }
          this.data = response.data
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Getting tenant list failed.',
            icon: 'report_problem'
          })
        })
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }
    this.getEdgeInfo()
    this.getTenants()
    this.intervalObj = setInterval(this.getTenants, POLLING_INTERVAL)
  },
  destroyed: function () {
    clearInterval(this.intervalObj)
  }
}
</script>
<style lang="stylus">
.tenant-card
  width 100%
</style>

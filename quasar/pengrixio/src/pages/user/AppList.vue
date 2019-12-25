<template>
  <q-page padding>
    <div
      class="fit row wrap justify-start content-start q-gutter-lg">
      <q-card bordered v-for="a in data" :key="a.name">
        <q-img :src="'statics/' + a.cat_logo" basic>
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
              <q-chip small icon="build" text-color="white"
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
          <q-btn icon="play_arrow" v-if="a.cat_type == 'vm'"
            flat round color="primary"
            @click="runApp(a.name, a.status)"
          >
            <q-tooltip
              content-class="bg-purple" content-style="font-size: 16px"
            >Run</q-tooltip>
          </q-btn>
          <q-btn icon="stop" v-if="a.cat_type == 'vm'"
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
  </q-page>
</template>

<script>
import { API_URL, POLLING_INTERVAL } from '../../config'
export default {
  name: 'AppList',
  data () {
    return {
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
          this.getApps()
          this.$q.notify({
            color: 'primary',
            position: 'bottom',
            message: 'Succeed to start the app ' + name,
            icon: 'report_problem'
          })
        })
        .catch(() => {
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
          this.getApps()
          this.$q.notify({
            color: 'primary',
            position: 'bottom',
            message: 'Succeed to stop the app ' + name,
            icon: 'report_problem'
          })
        })
        .catch((error) => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Fail to stop the app ' + name + ':' + error,
            icon: 'report_problem'
          })
        })
    },
    fullscreen: function () {
      if (document.documentElement.requestFullScreen) {
        document.documentElement.requestFullScreen();
      } else if (document.documentElement.mozRequestFullScreen) {
        document.documentElement.mozRequestFullScreen();
      } else if (document.documentElement.webkitRequestFullScreen) {
        document.documentElement.webkitRequestFullScreen();
      }
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
          window.open('http://' + this.broker, name, 'height=' + screen.height + ',width=' + screen.width + ',fullcreen=yes,addressbar=no')
          //window.location.href = 'http://' + this.broker
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
    getApps: function () {
      const url = API_URL + '/app/user/:' + this.$store.state.pengrixio.name + '/'
      this.$axios.get(url)
        .then((response) => {
          this.data = response.data
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Getting app list failed.',
            icon: 'report_problem'
          })
        })
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }
    this.getApps()
    this.intervalObj = setInterval(this.getApps, POLLING_INTERVAL)
  },
  destroyed: function () {
    clearInterval(this.intervalObj)
  }
}
</script>
<style lang="stylus">
</style>

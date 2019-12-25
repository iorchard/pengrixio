<template>
  <q-layout view="hHh Lpr fFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          round
          dense
          icon="menu"
          @click="leftDrawer = !leftDrawer"
        />
        <q-toolbar-title>KT Edge Platform (KEP)</q-toolbar-title>
        <q-btn
          v-if="this.$store.state.pengrixio.login"
          flat
          round
          dense
          icon="exit_to_app"
          @click="$router.replace('/logout/admin/')"
         />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawer"
      show-if-above
      side="left"
      elevated
      :width="200"
      :breakpoint="500"
      content-class="bg-grey-2"
    >
      <q-scroll-area class="fit q-pa-sm">
        <q-list padding>
          <q-item clickable v-ripple to="/dashboard/" exact>
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>Dashboard</q-item-section>
          </q-item>
          <q-expansion-item
            dense
            default-opened
            expand-separator
            icon="device_hub"
            label="Edge"
            clickable v-ripple to="/edge/" exact>
            <q-list padding>
              <q-item dense v-for="d in data" :key="d.name"
                clickable v-ripple :to="'/edge/' + d.name + '/'" exact>
                <q-item-section avatar>
                  <q-icon name="device_hub" size="xs" color="purple" />
                </q-item-section>
                <q-item-section>{{ d.name }}</q-item-section>
              </q-item>
            </q-list>
          </q-expansion-item>
          <q-item clickable v-ripple to="/tenant/" exact>
            <q-item-section avatar>
              <q-icon name="apartment" />
            </q-item-section>
            <q-item-section>Tenant</q-item-section>
          </q-item>
          <q-item clickable v-ripple to="/account/" exact>
            <q-item-section avatar>
              <q-icon name="people" />
            </q-item-section>
            <q-item-section>Account</q-item-section>
          </q-item>
          <q-item clickable v-ripple to="/catalog/" exact>
            <q-item-section avatar>
              <q-icon name="category" />
            </q-item-section>
            <q-item-section>App Hub</q-item-section>
          </q-item>
          <q-item clickable v-ripple to="/app/" exact>
            <q-item-section avatar>
              <q-icon name="apps" />
            </q-item-section>
            <q-item-section>Apps</q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
      <q-page-scroller position="bottom-right" :scroll-offset="150" :offset="[18, 18]">
        <q-btn fab icon="keyboard_arrow_up" color="accent" />
      </q-page-scroller>
    </q-page-container>

  </q-layout>
</template>

<script>
import { API_URL, POLLING_INTERVAL } from '../config'

export default {
  name: 'Main',

  data () {
    return {
      leftDrawer: true,
      miniState: true,
      data: []
    }
  },
  methods: {
    getEdges: function () {
      const url = API_URL + '/edge/'
      this.$axios.get(url)
        .then((response) => {
          this.data = response.data
          console.log(this.data)
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

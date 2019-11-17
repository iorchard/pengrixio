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
      :mini="miniState"
      @mouseover="miniState=false"
      @mouseout="miniState=true"
      side="left"
      elevated
      :width="200"
      :breakpoint="700"
      content-class="bg-grey-2"
    >
      <q-scroll-area class="fit q-pa-sm">
        <q-list padding>
          <q-item clickable v-ripple to="/edge/" exact>
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>Dashboard</q-item-section>
          </q-item>
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
            <q-item-section>Catalog</q-item-section>
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
    </q-page-container>

  </q-layout>
</template>

<script>
export default {
  name: 'Main',

  data () {
    return {
      leftDrawer: true,
      miniState: true
    }
  }
}
</script>

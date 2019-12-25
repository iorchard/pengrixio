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
        <q-toolbar-title>KT Edge Platform (KEP) VDI Service</q-toolbar-title>
        <div> Welcome, {{ username }}</div>
        <q-btn
          v-if="this.$store.state.pengrixio.login"
          flat
          round
          dense
          icon="exit_to_app"
          @click="$router.replace('/logout/')"
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
          <q-item clickable v-ripple to="/user/" exact>
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
      username: this.$store.state.pengrixio.name
    }
  }
}
</script>

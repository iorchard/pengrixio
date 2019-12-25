<template>
  <q-page padding>
    <form :action="broker" target="_self" ref="form"
      method="get">
    </form>
  </q-page>
</template>

<script>
import { API_URL } from '../../config'
// import { AppFullscreen } from 'quasar'
// import { openURL } from 'quasar'
export default {
  name: 'appConnect',
  data () {
    return {
      broker: ''
    }
  },
  methods: {
    connectBroker: function () {
      const url = API_URL + '/app/' + this.$route.params.name + '/connect/'
      this.$axios.get(url)
        .then((response) => {
          this.broker = response.data
          console.log(this.broker)
          // AppFullscreen.request()
          // openURL(this.broker)
          window.open(this.broker, this.$route.params.name, 'height=' + screen.height + ',width=' + screen.width + ',fullcreen=yes')
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Getting app info failed.',
            icon: 'report_problem'
          })
        })
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }
    this.connectBroker()
  }
}
</script>

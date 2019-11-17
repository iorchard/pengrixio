<template>
  <q-page padding>

    <form>
      <div class="q-pa-md">

        <div class="q-gutter-md" style="max-width:300px">
          <q-input v-model="form.name" label="Username" />
          <q-input v-model="form.pass" type="password"
            label="Enter Password" />
          <q-input v-model="form.pass2" type="password"
            label="Enter Password again" />
          <q-input v-model="form.cn" label="Name" />
          <q-select v-model="form.role" :options="form.roleOptions"
            hint="Role"/>
          <q-select v-model="form.state" :options="form.stateOptions"
            hint="State" />
          <q-select v-model="form.tenant" :options="form.tenantOptions"
            label="Tenant" hint="Tenant" />
          <q-input filled v-model="form.expireAt" hint="Expire date">
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy ref="qDateProxy" transition-show="scale"
                  transition-hide="scale">
                  <q-date v-model="form.expireAt"
                    @input="() => $refs.qDateProxy.hide()" />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
          <q-input v-model="form.desc" label="Description" />
        </div>
        <div>
          <q-btn label="Create" color="primary" @click="submit" />
        </div>
      </div>
    </form>

  </q-page>
</template>

<script>
import { API_URL, checkStrength } from '../../config'
import { sameAs, required, minLength, alphaNum } from 'vuelidate/lib/validators'
import moment from 'moment'

export default {
  name: 'accountCreate',
  data () {
    return {
      min: moment(new Date().toISOString()).format(),
      form: {
        name: '',
        pass: '',
        pass2: '',
        cn: '',
        role: 'user',
        roleOptions: ['admin', 'user'],
        state: 'Enabled',
        stateOptions: ['Enabled', 'Disabled', 'Locked'],
        tenant: [],
        tenantOptions: [],
        expireAt: moment(new Date().toISOString()).add(90, 'days').format(),
        desc: ''
      }
    }
  },
  validations: {
    form: {
      name: {
        required,
        alphaNum,
        minLength: minLength(3)
      },
      pass: {
        required,
        minLength: minLength(8)
      },
      pass2: {
        sameAsPassword: sameAs('pass')
      },
      cn: {
        required
      },
      expireAt: {
        required
      }
    }
  },
  methods: {
    submit: function () {
      if (!this.form.name) {
        this.$q.notify('Please enter User ID.')
        return
      }
      if (checkStrength(this.form.pass) < 3) {
        this.$q.notify('Please comply with password policy')
        return
      }
      if (this.form.pass !== this.form.pass2) {
        this.$q.notify('Passwords are not matched.')
        return
      }
      if (!this.form.cn) {
        this.$q.notify('Name is the necessary field.')
        return
      }
      if (!this.form.state) {
        this.$q.notify('State is the necessary field.')
        return
      }
      if (!this.form.expireAt) {
        this.$q.notify('Expire Date is the necessary field.')
        return
      }
      const payload = {
        name: this.form.name,
        pass: this.form.pass,
        cn: this.form.cn,
        role: this.form.role,
        state: this.form.state,
        tenant: this.form.tenant,
        expireAt: this.form.expireAt,
        desc: this.form.desc
      }
      const url = API_URL + '/account/'
      this.$axios.post(url, payload)
        .then((response) => {
          this.$router.push('/account/')
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Creating an account is failed.',
            icon: 'report_problem'
          })
        })
    },
    getTenants: function () {
      const url = API_URL + '/tenant/'
      this.$axios.get(url)
        .then((response) => {
          console.log(response.data)
          for (let i in response.data) {
            let r = response.data[i]
            this.form.tenantOptions.push(r.name)
          }
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'bottom',
            message: 'Getting tenant list is failed.',
            icon: 'report_problem'
          })
        })
    }
  },
  mounted: function () {
    if (!this.$store.state.pengrixio.login) { this.$router.push('/') }

    this.getTenants()
  }
}
</script>

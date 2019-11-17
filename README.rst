Pengrixio
==========

Pengrixio is a cloud/edge computing platform.

Tech stack
-----------

Backend API
++++++++++++

* Flask
* Connecxion: a framework on top of flask that handles HTTP request defined
  using OpenAPI(formerly known as Swagger)
* ETCD: key-value store
* Avro: data serialization system

Frontend JS
++++++++++++

* quasar: MIT licensed open source Vue.js based framework


API First Design



https://medium.com/@ryangordon210/building-python-microservices-part-i-getting-started-792fa615608

https://medium.com/adobetech/three-principles-of-api-first-design-fa6666d9f694

https://owncloud.org/news/running-owncloud-in-kubernetes-with-rook-ceph-storage/


vuelidate and quasar
---------------------

npm install vuelidate --save

quasar new boot vuelidate

vi boot/vuelidate.js
...
import Vuelidate from 'vuelidate'

export default ({ Vue }) => {
  Vue.use(Vuelidate)
}

vi quasar.conf.js
...
    boot: [
      'i18n',
      'axios',
      'vuelidate'
    ],


moment and quasar
------------------

npm install moment --save

quasar new boot moment

Apex Chart with quasar
------------------------

https://github.com/patrickmonteiro/quasar-apexcharts



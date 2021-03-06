
const routes = [
  {
    path: '/',
    component: () => import('layouts/Index.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') }
    ]
  },
  {
    path: '/dashboard/',
    component: () => import('layouts/Main.vue'),
    children: [
      { path: '', component: () => import('pages/Dashboard.vue') }
    ]
  },
  {
    path: '/user/',
    component: () => import('layouts/UserMain.vue'),
    children: [
      { path: '', component: () => import('pages/user/AppList.vue') }
    ]
  },
  {
    path: '/app/',
    component: () => import('layouts/Main.vue'),
    children: [
      { path: '', component: () => import('pages/app/List.vue') },
      { path: 'create/:user/', component: () => import('pages/app/Create.vue') },
      { path: 'connect/:name/', component: () => import('pages/app/Connect.vue') }
    ]
  },
  {
    path: '/catalog/',
    component: () => import('layouts/Main.vue'),
    children: [
      { path: '', component: () => import('pages/catalog/List.vue') },
      { path: 'create/', component: () => import('pages/catalog/Create.vue') },
      { path: ':name/edit/', component: () => import('pages/catalog/Edit.vue') }
    ]
  },
  {
    path: '/tenant/',
    component: () => import('layouts/Main.vue'),
    children: [
      { path: '', component: () => import('pages/tenant/List.vue') },
      { path: 'create/:edge_name/', component: () => import('pages/tenant/Create.vue') }
    ]
  },
  {
    path: '/edge/',
    component: () => import('layouts/Main.vue'),
    children: [
      { path: '', component: () => import('pages/edge/List.vue') },
      { path: 'create/', component: () => import('pages/edge/Create.vue') },
      { path: ':name/', component: () => import('pages/edge/Show.vue') },
      { path: ':name/edit/', component: () => import('pages/edge/Edit.vue') }
    ]
  },
  {
    path: '/project/',
    component: () => import('layouts/Main.vue'),
    children: [
      { path: '', component: () => import('pages/project/List.vue') }
    ]
  },
  {
    path: '/account/',
    component: () => import('layouts/Main.vue'),
    children: [
      { path: '', component: () => import('pages/account/List.vue') },
      { path: 'create/', component: () => import('pages/account/Create.vue') }
    ]
  },
  {
    path: '/login/',
    component: () => import('layouts/Index.vue'),
    children: [
      { path: '', component: () => import('pages/Login.vue') },
      { path: 'admin/', component: () => import('pages/LoginAdmin.vue') }
    ]
  },
  {
    path: '/logout/',
    component: () => import('layouts/Index.vue'),
    children: [
      { path: '', component: () => import('pages/Logout.vue') },
      { path: 'admin/', component: () => import('pages/LogoutAdmin.vue') }
    ]
  },
  {
    path: '/sample/',
    component: () => import('layouts/MyLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') }
    ]
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes

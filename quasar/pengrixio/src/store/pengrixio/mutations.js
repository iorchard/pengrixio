export const loggedIn = (state, bLogin) => {
  state.login = bLogin
}
export const setName = (state, sName) => {
  state.name = sName
}
export const setRole = (state, sRole) => {
  state.role = sRole
}
export const setToken = (state, sToken) => {
  state.token = sToken
}
export const setRefreshToken = (state, sRefreshToken) => {
  state.refreshToken = sRefreshToken
}

// // 设置登录状态的值
const mutations = {
    setLogin(state, payload) {
        state.user.isLogin = payload
    },
    setUserName(state, payload) {
        // state.user.username = payload
        state.user.name = payload
        window.localStorage.setItem("username", payload)
    },
    setIsSuperuser(state, payload) {
    state.user.is_superuser = payload
    window.localStorage.setItem("is_superuser", payload.toString())
  },
    updateCartCount(state, payload) {
        state.cartCount = payload.count;    // 设置到index
    }
}

export default mutations;

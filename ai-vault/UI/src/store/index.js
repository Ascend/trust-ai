import Vue from 'vue';
import Vuex from 'vuex';
import { getUserInfo } from '@/shared/common';
Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        login: {
            userInfo: getUserInfo()
        }
    },
    mutations: {
        userLogin(state, userInfo) {
            state.login.userInfo = userInfo;
        }
    },
    getters: {
        userInfo: (state) => state.login.userInfo,
    }
});
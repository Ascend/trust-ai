import Vue from 'vue';
import Vuex from 'vuex';
import { getUserInfo } from '@/shared/common';
Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        login: {
            userInfo: getUserInfo()
        },
      home: {
        version: '',
        tableData: [],
        isAhealth: false,
      }
    },
    mutations: {
      userLogin(state, userInfo) {
        state.login.userInfo = userInfo;
      },
      saveVersion(state, version) {
        state.home.version = version
      },
      saveHealth(state, health) {
        state.home.isAhealth = health
      },
      saveCert(state, data) {
        state.home.tableData = data
      }
    },
    getters: {
        userInfo: (state) => state.login.userInfo,
    }
});

<template>
  <div class="login-main">
    <div class="login-header">
      <img src="../assets/login-logo.png" />
      {{ $t('PLATFORM_TITLE') }}
    </div>
    <div class="login-block">
      <div class="subtitle">{{ $t('LOGIN_WELCOME') }}</div>
      <div class="title">{{ $t('MINDX_TITLE') }} {{ $t('PLATFORM_TITLE') }}</div>
      <input 
        v-model="username"
        type="text"
        required
        :placeholder="$t('PLACEHOLDER_USERNAME')"
        class="login-inp"
      />
      <input 
        v-model="password"
        type="password"
        required
        :placeholder="$t('PLACEHOLDER_PASSWORD')"
        class="login-inp"
        @keyup.enter="handleLogin"
      />
      <el-button type="primary" @click="handleLogin">{{ $t('SUBMIT') }}</el-button>
    </div>
  </div>
</template>

<script>
import { sendLogin } from '@/service/login'
import { saveAuthToken, saveAuthUserInfo } from '@/shared/common'
import { getUserInfo } from '../shared/common'
import store from '@/store'
export default {
  name: 'login',
  data () {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
    handleLogin() {
      let params = {
        UserName: this.username,
        Password: this.password,
      }
      sendLogin(params)
        .then(res => {
          if(res.data.status === '00000000') {
            saveAuthToken(res.data.data.Token);
            saveAuthUserInfo(res.data.data);
            store.commit('userLogin', getUserInfo())
            if (res.data.data.RoleID === 1){
              this.$router.push('/app/user')
            } else {
              this.$router.push('/app/ai-vault')
            }
            this.$message({
              message: this.$t('SUCCESS_LOGIN')
            })
          } else if(res.data.status === '21000004' || res.data.status === '00002000') {
              this.$message({
                  message: this.$t('ERR_LOGIN'),
              })
          } 
        })
        .catch(err => {
          if (err.code == 401) {
            this.$message({
              message: this.$t('ERR_LOGIN'),
              type: 'error'
            })
          } else if (err.code == 403) {
            this.$message({
              message: this.$t('ERR_LOGIN_LOCKING'),
              type: 'error'
            })
          } else {
            this.$message({
              message: err,
              type: 'error'
            })
          }
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login-main {
  width: 100vw;
  height: 100vh;
  background: url(../assets/bg_login.jpg) center no-repeat;
}

.login-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 50px;
  z-index: 1000;
  font-size: 22px;
  padding: 10px 30px;
  vertical-align: center;
  align-items: center;
  display: flex;
}

.login-header>img {
  height: 40px;
  margin-right: 20px;
}

.login-block {
  width: 396px;
  height: 500px;
  position: fixed;
  right: 140px;
  top: 12%;
  padding: 56px;
  background-color: #ffffff;
  box-shadow: 0 4px 16px 8px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.subtitle {
  font-size: 14px;
  color: #333a45;
  line-height: 16px;
  font-weight: 400;
  margin-bottom: 10px;
}

.title {
  font-size: 40px;
  color: #1f2329;
  line-height: 48px;
  font-weight: 600;
  margin-bottom: 50px;
}

.login-inp {
  height: 50px;
  width: 360px;
  display: block;
  margin-bottom: 20px;
  border: 1px solid #cbd4e2;
  border-radius: 2px;
  padding: 0 16px;
}

input::placeholder {
  font-size: 16px;
  color: #9097a3;
  line-height: 24px;
}

button {
  width: 396px;
  height: 50px;
  font-size: 16px;
  font-weight: 500;
  margin-top: 160px;
  color: #ffffff;
}
</style>

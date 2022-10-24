<template>
    <div class="header">
        <div>
            {{ $t('PLATFORM_TITLE')}}
        </div>
        <div class="header-user">
            <el-dropdown @command="handleCommand">
                <span class="el-dropdown-link">
                    <i class="el-icon-user"></i>
                    {{ username }}
                    <i class="el-icon-caret-bottom"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item command="change_password">{{ $t('CHANGE_PASSWORD') }}</el-dropdown-item>
                    <el-dropdown-item command="logout">{{ $t('LOGOUT') }}</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>
        <user-manage :isShow="isShow" @handleCancel="isShow = false" :currOperation="'changePassword'" />
    </div>
</template>

<script>
import UserManage from '@/components/UserManage.vue';
import { getUserInfo } from '@/shared/common'
import { logout } from '@/service/login'

export default {
    components: {
        UserManage
    },
    data() {
        return {
            username: getUserInfo().UserName,
            isShow: false,
        };
    },
    mounted() {

    },
    methods: {
        handleCommand(command) {
            if (command === 'change_password') {
                this.handleOpenChangePassword()
            } else if (command === 'logout') {
                this.handleLogout()
            }
        },
        handleLogout() {
            logout()
                .then(res => {
                    if (res.data.status === '00000000') {
                        sessionStorage.clear()
                        this.$router.push('/login');
                    }
                })
            this.$router.push('/login');
        },
        handleOpenChangePassword() {
            this.isShow = true
        },
    }
}
</script>
<style>
.header {
    color: #A8A8A8;
    box-shadow: inset 0 -2px 0 0 #2a2f37;
    font-size: 22px;
    padding-left: 30px;
    vertical-align: center;
    align-items: center;
    height: 50px;
    display: flex;
    background-color: #181b20;
}

.header-user {    
    position: fixed;
    right: 40px;
}

/* .inp-psw {
    width: 80%;
} */
</style>
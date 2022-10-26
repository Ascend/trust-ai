<template>
    <div>
        <template v-for="nav in navList">
            <div class="nav-item" v-if="nav.isShow" @click="jumpNav(nav)">
                <div class="nav-wrap">
                    <img :src="require('@/assets/icon/'+nav.icon)" class="nav-icon"/>
                    <span class="nav-text">{{ $t(nav.label) }}</span>
                </div>
            </div>
        </template>
    </div>
</template>

<script>
import store from '@/store'

export default {
    components: {},
    data() {
        return {
            navList: [
                {
                    id: 'home',
                    label: 'NAV_HOME',
                    href: 'home',
                    icon: 'icon_home.png',
                    isShow: false,
                },
                {
                    id: 'user',
                    label: 'NAV_USER',
                    href: 'user',
                    icon: 'icon_user.png',
                    isShow: false,
                },
                {
                    id: 'ai-vault',
                    label: 'NAV_AI_VAULT',
                    icon: 'icon_ai_vaul.png',
                    href: 'ai-vault',
                    isShow: false,
                },
            ],
            currentPath: '',
        };
    },
    mounted() {
        this.getMenuList()
    },
    methods: {
        jumpNav(item) {
            if(this.currentPath !== item.href){
                this.currentPath = item.href
                this.$router.push({ name: item.href })
            }
        },
        getMenuList() {
            let roleId = store.state.login.userInfo.RoleID;
            if(roleId === 1) {
                this.navList[0].isShow = true
                this.navList[1].isShow = true
            } else {
                this.navList[2].isShow = true
            }

        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.nav-item {
    height: 32px;
    width: 200px;
    padding-top: 10px;
    padding-left: 20px;
    border-radius: 10px;
    background: #1f2329;
    margin-bottom: 10px;
}

.nav-item {
    cursor: pointer;
}

.nav-icon {
    vertical-align: middle;
}

.nav-text {
    font-size: 12px;
    line-height: 16px;
    font-weight: 400;
    vertical-align: middle;
    color: #FFFFFE;
}
</style>

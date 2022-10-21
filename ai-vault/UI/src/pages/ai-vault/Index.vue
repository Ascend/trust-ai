<template>
    <div>
        <add-key 
            :isAddKey="isAddKey"
            :currPage="activeName"
            @handleCancelAdd="handleCancelAdd"
            @handleRefresh="handleRefresh"
        ></add-key>
        <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane name="mk">
                <span slot="label">{{ $t('TAB_MAIN_KEY') }}</span>
                <div class="tab-main">
                    <main-key @handleAddMK="handleAddKey" :currPage="activeName" :isRefresh="isRefreshMK" />
                </div>                
            </el-tab-pane>
            <el-tab-pane name="psk">
                <span slot="label">{{ $t('TAB_PRE_KEY') }}</span>
                <div class="tab-main">
                    <pre-shared-key @handleAddPSK="handleAddKey" :currPage="activeName" :isRefresh="isRefreshPSK" />
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import AddKey from '@/pages/ai-vault/AddKey.vue';
import MainKey from '@/pages/ai-vault/MainKey.vue'
import PreSharedKey from '@/pages/ai-vault/PreSharedKey.vue'

export default {
    components: {
        AddKey,
        MainKey,
        PreSharedKey
    },
    name: 'ai-vault',
    data() {
        return {
            isAddKey: false,
            activeName: 'mk',
            isRefreshMK: true,
            isRefreshPSK: true,
        };
    },
    mounted() {
    },
    methods: {
        handleClick(tab, event) {
            this.isAddKey = false
        },
        handleAddKey() {
            this.isAddKey = true
        },
        handleAddPSK() {
            // ....
        },
        handleRefresh(currRefreshPage) {
            if(currRefreshPage === 'mk'){
                this.isRefreshMK = !this.isRefreshMK
            } else {
                this.isRefreshPSK = !this.isRefreshPSK
            }
        },
        handleCancelAdd() {
            this.isAddKey = false
        }
    }
}
</script>

<style scoped>
.tab-main {
    background-color: #1f2329;
    height: calc(100vh - 194px);
    border-radius: 4px;
    padding: 24px;
}
</style>
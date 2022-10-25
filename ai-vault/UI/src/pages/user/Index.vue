<template>
    <div style="margin-bottom: 20px;">
        <div class="user-operation">
            <el-button
                  type="primary"
                  plain
                  @click="handleConfirmAddUser"
              >
                  {{ $t('BUTTON_ADD_USER') }}
            </el-button>
            <el-input
                type="text"
                prefix-icon="el-icon-search"
                v-model="UserName"
                class="input-search"
                :placeholder="$t('PLACEHOLDER_INPUT')"
                clearable
                @clear="handleClear"
                @keyup.enter.native="fetchUserList"
            ></el-input>
            <el-button
                icon="el-icon-refresh"
                class="button-refresh"
                @click="fetchUserList"
            ></el-button>
        </div>

        <el-table
            :data="userData"
            style="width: 100%; margin-top: 40px; margin-bottom: 20px;"
            :cell-style="{ textAlign: 'center', border: '0.5px solid rgb(123, 143, 175, 0.5)', padding: '10px 0', }"
            :header-cell-style="{ textAlign: 'center', padding: '10px 0', }"
            :empty-text="$t('EMPTY_TEXT')"
        >
            <el-table-column prop="UserID" :label="$t('COLUMN_USER_ID')"></el-table-column>
            <el-table-column prop="UserName" :label="$t('COLUMN_USER_NAME')"></el-table-column>
            <el-table-column prop="Role" :label="$t('COLUMN_USER_TYPE')"></el-table-column>
            <el-table-column prop="CreateTime" :label="$t('COLUMN_CREATE_TIME')"></el-table-column>
            <el-table-column prop="operation" :label="$t('COLUMN_OPERATION')" width="120">
                <template slot-scope="scope">
                    <el-button @click="handleConfirmDelete(scope.row)" type="danger" :disabled="scope.row.RoleID === 1" plain size="small">
                        {{ $t('OPERATION_DELETE') }}
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :total="userPagination.total"
            :page-size="userParams.PageSize"
            layout="prev, pager, next"
            style="padding-bottom: 30px;"
        >
        </el-pagination>

        <el-dialog
            :title="$t('CONFIRM_DELETE')"
            :visible.sync="isDelete"
            width="28%"
            :close-on-click-modal="false"
            :modal="false"
        >
            {{$t('CONFIRM_DELETE_TIP')}} {{ selectedRow.UserName }}?
            <span slot="footer" class="dialog-footer">
                <el-button @click="isDelete = false">{{$t('BTN_CANCEL')}}</el-button>
                <el-button type="primary" @click="handleDelete">{{$t('BTN_OK')}}</el-button>
            </span>
        </el-dialog>

        <user-manage :isShow="isAddUser" @handleCancel="handleCancel" :currOperation="'addUser'" />
    </div>
</template>

<script>
import { fetchUser, deleteUser } from '@/service/user.js'
import UserManage from '@/components/UserManage.vue';

export default {
    components: {
        UserManage,
    },
    name: 'user',
    data() {
        return {
            userData: [],
            userPagination: {
                total: 0,
            },
            userParams: {
                CurrentPage: 1,
                PageSize: 10,
            },
            isDelete: false,
            selectedRow: {},
            isAddUser: false,
            UserName: '',
        };
    },
    mounted() {
      this.fetchUserList()
    },
    methods: {
        fetchUserList() {
            if(this.UserName.length > 0) {
                this.userParams.UserName = this.UserName
            } else {
                delete this.userParams.UserName
            }
            fetchUser(this.userParams)
                .then(res => {
                    res.data.data.users.forEach(item => {
                        // RoleID = 1:管理员，=4 普通用户
                        item.Role = {1: '管理员', 4: '普通用户'}[item.RoleID]
                    })
                    this.userData = res.data.data.users
                    this.userPagination.total = res.data.data.total
                })
        },
        handleConfirmDelete(row) {
            this.selectedRow = row
            this.isDelete = true
        },
        handleDelete(){
            deleteUser(this.selectedRow.UserName)
                .then(res => {
                    if(res.data.status === '00000000') {
                        this.$message({
                            message: this.$t('SUCCESS_DELETE'),
                        })
                        this.isDelete = false
                        this.fetchUserList()
                    }else if(res.data.status === '21000001') {
                        this.$message({
                            message: this.$t('ERR_DELETE') + '。' + this.$t('ERR_CONNECT_AIVAULT'),
                        })
                        this.isDelete = false
                    } else{
                        this.$message({
                            message: this.$t('ERR_DELETE') + '。' + this.$t('ERR_DELETE_USER'),
                        })
                        this.isDelete = false
                    }
                })
                .catch(err => {
                    this.isDelete = false
                })
        },
        handleConfirmAddUser() {
            this.isAddUser = true
        },
        handleCancel() {
            this.isAddUser = false
            this.fetchUserList()
        },
        handleSizeChange(val) {
            this.userParams.PageSize = val
            this.fetchUserList()
        },
        handleCurrentChange(val) {
            this.userParams.CurrentPage = val
            this.fetchUserList()
        },
        handleClear() {
            this.fetchUserList()
        }
    }
}
</script>
<style scoped>
.user-operation {
    display: flex;
    align-items: center;
    float: right;
    margin-bottom: 10px;
}

.input-search {
    width: 280px;
    margin-left: 10px;
}

.button-refresh {
    margin-left: 10px;
}
</style>

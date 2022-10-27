<template>
    <div style="margin-bottom: 20px;">
      <div class="user-amount">
            {{ $t('NAV_USER') }}
        </div>

        <div class="file-body-top">
        <div class="menu">
          <div class="name-wrapper">
          <img class="back-up" src="@/assets/icon/icon_user_amount.png" />
        <div class="margin">{{ $t('USER_AMOUNT') }}</div>
         <div class="num"> {{ useramount }} </div>
        </div>
          </div>
             </div>

        <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              class="button-add"
              @click="handleConfirmAddUser"
          >
                  {{ $t('BUTTON_ADD_USER') }}
         </el-button>

        <div class="user-operation">
            <el-input
                type="text"
                prefix-icon="el-icon-search"
                v-model="UserName"
                class="input-search"
                :placeholder="$t('PLACEHOLDER_INPUT')"
                clearable
                @clear="handleClear"
                @keyup.enter.native="handleSearch"
            ></el-input>
            <el-button
                icon="el-icon-refresh"
                class="button-refresh"
                @click="handleSearch"
            ></el-button>
        </div>

        <div style="background:#1f2329; margin-top: 70px;">
            <el-table
                :data="userData"
                style="width: 100%; margin-top: 40px; margin-bottom: 5px; font-size: 12px; border-radius: 4px;padding: 24px;"
                :cell-style="{ textAlign: 'center', padding: '10px 0', }"
                :header-cell-style="{ textAlign: 'center', padding: '10px 0', }"
                :empty-text="$t('EMPTY_TEXT')"
                :height="tableHeight"
                @sort-change="handleSortUserTable"
            >
                <el-table-column prop="UserID" :label="$t('COLUMN_USER_ID')" sortable="custom"></el-table-column>
                <el-table-column prop="UserName" :label="$t('COLUMN_USER_NAME')"></el-table-column>
                <el-table-column prop="Role" :label="$t('COLUMN_USER_TYPE')"></el-table-column>
                <el-table-column prop="CreateTime" :label="$t('COLUMN_CREATE_TIME')" sortable="custom"></el-table-column>
                <el-table-column prop="operation" :label="$t('COLUMN_OPERATION')" width="240">
                    <template slot-scope="scope">
                        <el-button @click="handleConfirmReset(scope.row)" type="text" :disabled="scope.row.RoleID === 1" size="small">
                            {{ $t('RESET_PASSWORD') }}
                        </el-button>
                        <el-button @click="handleConfirmDelete(scope.row)" type="text" :disabled="scope.row.RoleID === 1" size="small">
                            {{ $t('OPERATION_DELETE') }}
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page.sync="pageParams.CurrentPage"
                :page-size="pageParams.PageSize"
                :total="userPagination.total"
                layout="total, prev, pager, next, jumper"
                style="padding-bottom: 20px;"
            >
            </el-pagination>
        </div>

        <el-dialog
            :title="indexOperation === 'resetPWD' ? $t('RESET_PASSWORD') : $t('CONFIRM_DELETE')"
            :visible.sync= "isDelorReset"
            width="28%"
            :close-on-click-modal="false"
            :modal="false"
        >
            <el-form v-if="indexOperation === 'resetPWD'" :model="resetPswForm" :rules="resetPswRules" ref="resetPswForm">
                <el-form-item :label="$t('NEW_PSW')" prop="NewPassword" :label-width="formLabelWidth">
                    <el-tooltip :content="$t('TIP_PASSWORD')" placement="right">
                        <el-input v-model="resetPswForm.NewPassword" type="password" class="input-psw" :placeholder="$t('PLACEHOLDER_NEW_PASSWORD')" autocomplete="off"></el-input>
                    </el-tooltip>
                </el-form-item>
                <el-form-item :label="$t('CONFIRM_PSW')" prop="NewPasswordConfirm" :label-width="formLabelWidth">
                    <el-tooltip :content="$t('TIP_PASSWORD')" placement="right">
                        <el-input v-model="resetPswForm.NewPasswordConfirm" @keyup.enter.native="handleSubmitResetPassword()" type="password" class="input-psw" :placeholder="$t('PLACEHOLDER_CONFIRM_PASSWORD')" autocomplete="off"></el-input>
                    </el-tooltip>
                </el-form-item>
            </el-form>
            <div v-else class="dialog-tip">
                <div style="margin-left: 16px; margin-right: 16px"><img src="@/assets/icon/warn.svg"></div>
                {{$t('CONFIRM_DELETE_TIP')}}: {{ selectedRow.UserName }}?
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button class="dialog-button" @click="isDelorReset = false">{{$t('BTN_CANCEL')}}</el-button>
                <el-button class="dialog-button" type="primary" @click="indexOperation === 'resetPWD' ? handleSubmitResetPassword() : handleDelete()">{{$t('BTN_OK')}}</el-button>
            </span>
        </el-dialog>

        <user-manage :isShow="isAddUser" @handleCancel="handleCancel" :currOperation="'addUser'" />
    </div>
</template>

<script>
import { fetchUser, deleteUser, resetPassword } from '@/service/user.js'
import UserManage from '@/components/UserManage.vue';

export default {
    components: {
        UserManage,
    },
    name: 'user',
    data() {
        let checkConfirmNewUserPassword = (rule, value, callback) => {
            if (value !== this.resetPswForm.NewPassword) {
                callback(new Error(this.$t('ERR_CANNOT_CONFIRM_NEW_PASSWORD')))
            } else {
                callback();
            }
        }

        return {
            useramount: 0,
            userData: [],
            userPagination: {
                total: 10,
            },
            sortParams: {
                SortBy: 'UserID',
                SortMode: 'asc',
            },
            pageParams: {
                CurrentPage: 1,
                PageSize: 10,
            },
            resetPswForm: {
                UserName: '',
                NewPassword: '',
                NewPasswordConfirm: '',
            },
            formLabelWidth: '100px',
            selectedRow: {},
            isDelorReset: false,
            indexOperation: '',
            isAddUser: false,
            UserName: '',
            resetPswRules: {
                NewPassword: [
                    { required: true, message: this.$t('PLACEHOLDER_NEW_PASSWORD'), trigger: 'blur' },
                ],
                NewPasswordConfirm: [
                    { required: true, message: this.$t('PLACEHOLDER_CONFIRM_PASSWORD'), trigger: 'blur' },
                    { validator: checkConfirmNewUserPassword, trigger: 'blur' }
                ]
            },
            tableHeight: window.innerHeight - 330
        };
    },
    watch: {
        isDelorReset(newValue, oldValue) {
            if(this.indexOperation === 'resetPWD'){
                this.$nextTick(()=>{
                    this.$refs.resetPswForm.resetFields();
                })
            }
        }
    },
    mounted() {
      this.fetchUserList()
    },
    methods: {
        fetchUserList() {
            let params = {
                PageSize: 10,
                CurrentPage: this.pageParams.CurrentPage,
                SortBy: this.sortParams.SortBy,
                SortMode: this.sortParams.SortMode,
            }
            if(this.UserName.length > 0) {
                params.UserName = this.UserName
            }
            fetchUser(params)
                .then(res => {
                    res.data.data.users.forEach(item => {
                        item.Role = {1: '管理员', 4: '普通用户'}[item.RoleID]
                    })
                    this.userData = res.data.data.users
                    this.userPagination.total = res.data.data.total
                })
            this.handleGetUserAmount()
        },
        handleConfirmDelete(row) {
            this.selectedRow = row
            this.indexOperation = "delUser"
            this.isDelorReset = true
        },
        handleConfirmReset(row) {
            this.selectedRow = row
            this.indexOperation = "resetPWD"
            this.isDelorReset = true
        },
        handleSubmitResetPassword() {
            this.$refs.resetPswForm.validate((valid) => {
                if (valid) {
                    this.resetPswForm.UserName = this.selectedRow.UserName
                    resetPassword(this.resetPswForm)
                        .then(res => {
                            if(res.data.status === '00000000') {
                                this.$message.success({
                                    message: this.$t('SUCCESS_RESET_PASSWORD')
                                })
                                this.isDelorReset = false
                                this.fetchUserList()
                            } else if (res.data.status === '00002000') {
                                this.$message.error({
                                    message: this.$t('ERR_PARAMS_CHECK_FAILED'),
                                })
                            } else {
                                this.$message.error({
                                    message: this.$t('ERR_RESET_PASSWORD'),
                                })
                            }
                        })
                        .catch(err => {
                            this.isDelorReset = false
                        })
                }
            })
        },
        handleDelete(){
            deleteUser(this.selectedRow.UserName)
                .then(res => {
                    if(res.data.status === '00000000') {
                        this.$message.success({
                            message: this.$t('SUCCESS_DELETE'),
                        })
                        this.isDelorReset = false
                        this.fetchUserList()
                    }else if(res.data.status === '21000001') {
                        this.$message.error({
                            message: this.$t('ERR_DELETE') + '。' + this.$t('ERR_CONNECT_AIVAULT'),
                        })
                    } else{
                        this.$message.error({
                            message: this.$t('ERR_DELETE') + '。' + this.$t('ERR_DELETE_USER'),
                        })
                    }
                })
                .catch(err => {
                    this.isDelorReset = false
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
            this.pageParams.PageSize = val
            this.fetchUserList()
        },
        handleCurrentChange(val) {
            this.pageParams.CurrentPage = val
            this.fetchUserList()
        },
        handleSearch() {
            this.pageParams.CurrentPage = 1
            this.fetchUserList()
        },
        handleClear() {
            this.pageParams.CurrentPage = 1
            this.fetchUserList()
        },
        handleSortUserTable({column, prop, order}){
            this.sortParams.SortBy = prop === 'UserID' ? 'UserID' : prop
            this.sortParams.SortMode = {'ascending': 'asc', 'descending': 'desc'}[order]
            this.fetchUserList()
        },
        handleGetUserAmount() {
            fetchUser({})
                .then(res => {
                        this.useramount = res.data.data.total
                    })
        }
    }
}
</script>

<style scoped>
.file-body-top{
  display: flex;
  margin-bottom: 16px;
}

.menu{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    min-width: 200px;
    max-width: 400px;
    height: 56px;
    padding-left: 25px;
    padding-right: 24px;
    border-radius: 4px;
    margin-right: 16px;
    font-size: 12px;
    line-height: 16px;
    flex: 1;
    flex-shrink: 0;
    background: #333333;
}
.menu:last-child{
    margin-right: 0;
}


.name-wrapper {
    display: flex;
    align-items: center;
    font-weight: 500;
    color: #FFFFFE;
}
.back-up {
      width: 20px;
      height: 24px;
      margin-right: 8px;
    }

.num{
    font-size: 12px;
    color: #FFFFFE;
    letter-spacing: 0;
    text-align: right;
    line-height: 24px;
    font-weight: 700;
    margin-left: 300px;
  }

.button-add {
    border-radius: 2px;
    font-size: 12px;
    float: left;
    font-size: 12px;
    color: #FFFFFF;
    letter-spacing: 0;
    text-align: center;
    line-height: 16px;
    font-weight: 500;
}

.margin {
  margin-left: 8px;
}

.user-operation {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    float: right;
}

.input-search {
    width: 280px;
    margin-left: 10px;
}

.button-refresh {
    margin-left: 10px;
}

.input-psw {
    width: 80%;
}

.user-amount {
    margin-bottom: 10px;
    font-size: 16px;
    color: #FFFFFE;
    line-height: 24px;
    font-weight: 500;
}

.el-table::before {
    background-color: #1f2329;
}

</style>

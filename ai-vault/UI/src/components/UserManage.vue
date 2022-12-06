<template>
    <el-dialog
        :title="currOperation === 'changePassword' ? $t('CHANGE_PASSWORD') : $t('BUTTON_ADD_USER')"
        :visible.sync="isShow"
        width="28%"
        :close-on-click-modal="false"
        :modal="false"
        :before-close="handleClose"
    >
        <div v-if="currOperation === 'addUser'">
            <div style="background: rgba(0,119,255,0.2); border-radius: 2px; display: flex; padding-bottom: 8px; padding-top: 8px; margin-bottom: 24px">
                <div style="margin-left: 8px;"><img src="@/assets/icon/remind.svg"></div>
                <div style="margin-left: 8px;">{{ $t('ADD_USER_TIP')}}</div>
            </div>
            <el-form  :model="addUserForm" :rules="addUserRules" ref="addUserForm">
                <el-form-item :label="$t('COLUMN_USER_NAME')" prop="UserName" :label-width="formLabelWidth">
                    <el-tooltip :content="$t('TIP_ADD_USER_USERNAME')" placement="right">
                        <el-input v-model="addUserForm.UserName" class="inp-psw" :placeholder="$t('PLACEHOLDER_USERNAME')" autocomplete="off"></el-input>
                    </el-tooltip>
                </el-form-item>
                <el-form-item :label="$t('NEW_PSW')" prop="Password" :label-width="formLabelWidth">
                    <el-tooltip :content="$t('TIP_PASSWORD')" placement="right">
                        <el-input v-model="addUserForm.Password" type="password" class="inp-psw" :placeholder="$t('PLACEHOLDER_CURRENT_PASSWORD')" autocomplete="off"></el-input>
                    </el-tooltip>
                </el-form-item>
                <el-form-item :label="$t('CONFIRM_PSW')" prop="PasswordConfirm" :label-width="formLabelWidth">
                    <el-tooltip :content="$t('TIP_PASSWORD')" placement="right">
                        <el-input v-model="addUserForm.PasswordConfirm" @keyup.enter.native="handleSubmitAddUser('addUserForm')" type="password" class="inp-psw" :placeholder="$t('PLACEHOLDER_CONFIRM_PASSWORD')" autocomplete="off"></el-input>
                    </el-tooltip>
                </el-form-item>
            </el-form>
        </div>
        <el-form v-else :model="changePswForm" :rules="changePswRules" ref="changePswForm">
            <el-form-item :label="$t('CURRENT_PSW')" prop="Password" :label-width="formLabelWidth">
                <el-input v-model="changePswForm.Password" type="password" class="inp-psw" :placeholder="$t('PLACEHOLDER_CURRENT_PASSWORD')" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item :label="$t('NEW_PSW')" prop="NewPassword" :label-width="formLabelWidth">
                <el-tooltip :content="$t('TIP_PASSWORD')" placement="right">
                    <el-input v-model="changePswForm.NewPassword" type="password" class="inp-psw" :placeholder="$t('PLACEHOLDER_NEW_PASSWORD')" autocomplete="off"></el-input>
                </el-tooltip>
            </el-form-item>
            <el-form-item :label="$t('CONFIRM_PSW')" prop="NewPasswordConfirm" :label-width="formLabelWidth">
                <el-tooltip :content="$t('TIP_PASSWORD')" placement="right">
                    <el-input v-model="changePswForm.NewPasswordConfirm" @keyup.enter.native="handleSubmitChangePassword('changePswForm')" type="password" class="inp-psw" :placeholder="$t('PLACEHOLDER_CONFIRM_PASSWORD')" autocomplete="off"></el-input>
                </el-tooltip>
            </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button v-no-more-click class="dialog-button" @click="handleCancel">{{$t('BTN_CANCEL')}}</el-button>
            <el-button v-no-more-click class="dialog-button" type="primary" @click="currOperation === 'addUser' ? handleSubmitAddUser('addUserForm') : handleSubmitChangePassword('changePswForm')">{{$t('BTN_OK')}}</el-button>
        </span>
    </el-dialog>
</template>

<script>
import { getUserInfo } from '@/shared/common'
import { changePassword, addUser } from '@/service/user.js'
import { logout } from '@/service/login'

export default {
    name: 'UserManager',
    components: {
    },
    props: {
        isShow: Boolean,
        currOperation: String,
    },
    data() {
        let checkConfirmNewUserPassword = (rule, value, callback) => {
            if (value !== this.addUserForm.Password) {
                callback(new Error(this.$t('ERR_CANNOT_CONFIRM_NEW_PASSWORD')))
            } else {
                callback();
            }
        }

        let checkNewPassword = (rule, value, callback) => {
            if (value == this.changePswForm.Password) {
                callback(new Error(this.$t('ERR_SAME_CURRENT_PASSWORD')))
            } else {
                callback();
            }
        }

        let checkConfirmPassword = (rule, value, callback) => {
            if (value !== this.changePswForm.NewPassword) {
                callback(new Error(this.$t('ERR_CANNOT_CONFIRM_NEW_PASSWORD')))
            } else {
                callback();
            }
        }
        return {
            username: getUserInfo().UserName,
            isChangePassword: false,
            addUserForm: {
                UserName: '',
                Password: '',
                PasswordConfirm: '',
            },
            changePswForm: {
                Password: '',
                NewPassword: '',
                NewPasswordConfirm: '',
            },
            formLabelWidth: '100px',
            addUserRules: {
                UserName: [
                    { required: true, message: this.$t('PLACEHOLDER_USERNAME'), trigger: 'blur' },
                ],
                Password: [
                    { required: true, message: this.$t('PLACEHOLDER_CURRENT_PASSWORD'), trigger: 'blur' },
                ],
                PasswordConfirm: [
                    { required: true, message: this.$t('PLACEHOLDER_CONFIRM_PASSWORD'), trigger: 'blur' },
                    { validator: checkConfirmNewUserPassword, trigger: 'blur' }
                ]
            },
            changePswRules: {
                Password: [
                    { required: true, message: this.$t('PLACEHOLDER_CURRENT_PASSWORD'), trigger: 'blur' },
                ],
                NewPassword: [
                    { required: true, message: this.$t('PLACEHOLDER_NEW_PASSWORD'), trigger: 'blur' },
                    { validator: checkNewPassword, trigger: 'blur' }
                ],
                NewPasswordConfirm: [
                    { required: true, message: this.$t('PLACEHOLDER_CONFIRM_PASSWORD'), trigger: 'blur' },
                    { validator: checkConfirmPassword, trigger: 'blur' }
                ]
            }
        };
    },
    watch: {
        isShow(newValue, oldValue) {
            let formName = this.currOperation === 'addUser' ? 'addUserForm' : 'changePswForm'
            this.$nextTick(()=>{
                this.$refs[formName].resetFields();
            })
        }
    },
    mounted() {

    },
    methods: {
        handleSubmitChangePassword(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    changePassword(this.changePswForm)
                        .then(res => {
                            if(res.data.status === '00000000') {
                                this.$message.success({
                                    message: this.$t('SUCCESS_CHANGE_PASSWORD'),
                                })
                                this.handleCancel()
                                setTimeout(() => {
                                    logout()
                                    .then(res => {
                                        if (res.data.status === '00000000') {
                                            sessionStorage.clear()
                                            this.$router.push('/login');
                                        }
                                    })
                                    sessionStorage.clear()
                                    this.$router.push('/login');
                                }, 2000)
                            } else if (res.data.status === '00002000') {
                                this.$message.error({
                                    message: this.$t('ERR_PARAMS_CHECK_FAILED'),
                                })
                            } else {
                                this.$message.error({
                                    message: this.$t('ERR_CHANGE_PASSWORD'),
                                })
                            }
                        })
                        .catch(err => {
                            this.handleCancel()
                        })
                } else {
                    return false
                }
            })
        },
        handleSubmitAddUser(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    addUser(this.addUserForm)
                        .then(res => {
                            if(res.data.status === '00000000') {
                                this.$message.success({
                                    message: this.$t('SUCCESS_ADD_USER'),
                                })
                                this.handleCancel()
                            } else if (res.data.status === '21000003') {
                                this.$message.error({
                                    message: this.$t('ERR_USER_AREADY_EXIST'),
                                })
                            } else if (res.data.status === '21000006') {
                                this.$message.error({
                                    message: this.$t('ERR_USER_NUM_EXCEED'),
                                })
                            } else if (res.data.status === '00002000') {
                                this.$message.error({
                                    message: this.$t('ERR_PARAMS_CHECK_FAILED'),
                                })
                            } else {
                                this.$message.error({
                                    message: this.$t('ERR_ADD_USER'),
                                })
                            }
                        })
                        .catch(err => {
                            this.handleCancel()
                        })
                } else {
                    return false
                }
            })
        },
        handleCancel() {
            this.$emit('handleCancel')
        },
        handleClose() {
            this.$emit('handleCancel')
        },
    }
}
</script>
<style scoped>
.inp-psw {
    width: 80%;
}
</style>

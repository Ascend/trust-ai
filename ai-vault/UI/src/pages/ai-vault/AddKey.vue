<template>
    <div>
        <el-dialog
            :title="currPage === 'mk' ? $t('ADD_MK') : $t('ADD_PSK')"
            :visible.sync="isAddKey"
            :close-on-click-modal="false"
            :before-close="handleClose"
            width="30%"
            :modal="false"
        >
            <div v-if="currPage === 'mk'" style="background: rgba(249,118,17,0.2);border-radius: 2px;display: flex; padding-bottom: 8px; padding-top: 8px; margin-bottom: 24px">
                <div style="margin-left: 8px"><img src="@/assets/icon/alarm-orange.svg"></div>
                <div style="margin-left: 8px">{{ $t('ADD_MK_TIP')}}</div>
            </div>
            <div v-else style="background: rgba(0,119,255,0.2);border-radius: 2px;display: flex; padding-bottom: 8px; padding-top: 8px; margin-bottom: 24px">
                <div style="margin-left: 8px"><img src="@/assets/icon/remind.svg"></div>
                <div style="margin-left: 8px">{{ $t('ADD_PSK_TIP')}}</div>
            </div>
            <el-form v-if="currPage === 'mk'" :model="mkForm" :rules="mkRules" ref="mkForm">
                <el-form-item :label="$t('KEY_NAME')" prop="MKName" :label-width="formLabelWidth">
                    <el-tooltip :content="$t('TIP_KEY_NAME')" placement="right">
                        <el-input v-model="mkForm.MKName" class="inp-add" :placeholder="$t('PLACEHOLDER_KEY_NAME')" autocomplete="off"></el-input>
                    </el-tooltip>
                </el-form-item>
                <el-form-item prop="MKUsage" :label="$t('KEY_USAGE')" :label-width="formLabelWidth">
                    <el-tooltip :content="$t('TIP_KEY_USAGE')" placement="right">
                        <el-input v-model="mkForm.MKUsage" class="inp-add" :placeholder="$t('PLACEHOLDER_KEY_USAGE')" autocomplete="off"></el-input>
                    </el-tooltip>
                </el-form-item>
                <el-form-item :label="$t('USER_PASSWORD')" prop="Password" :label-width="formLabelWidth">
                    <el-tooltip :content="$t('TIP_KEY_PASSWORD')" placement="right">
                        <el-input v-model="mkForm.Password" type="password" show-password class="inp-add" :placeholder="$t('PLACEHOLDER_MK_PASSWORD')" autocomplete="off"></el-input>
                    </el-tooltip>
                </el-form-item>
                <el-form-item :label="$t('COMMENT')" prop="MKRemarks" :label-width="formLabelWidth">
                    <el-tooltip :content="$t('TIP_REMARKS')" placement="right">
                        <el-input v-model="mkForm.MKRemarks" type="textarea" show-word-limit maxlength="256" class="inp-add" :placeholder="$t('PLACEHOLDER_COMMENT')" autocomplete="off"></el-input>
                    </el-tooltip>
                </el-form-item>
            </el-form>

            <el-form v-else :model="pskForm" :rules="pskRules" ref="pskForm">
                <el-form-item :label="$t('PSK_NAME')" prop="PSKName" :label-width="formLabelWidth">
                    <el-tooltip :content="$t('TIP_KEY_NAME')" placement="right">
                        <el-input v-model="pskForm.PSKName" class="inp-add" :placeholder="$t('PLACEHOLDER_PSK_NAME')" autocomplete="off"></el-input>
                    </el-tooltip>
                </el-form-item>
                <el-form-item :label="$t('MK_NAME')" prop="MKName" :label-width="formLabelWidth">
                    <el-tooltip :content="$t('TIP_KEY_NAME')" placement="right">
                        <el-input v-model="pskForm.MKName" class="inp-add" :placeholder="$t('PLACEHOLDER_MK_NAME')" autocomplete="off"></el-input>
                    </el-tooltip>
                </el-form-item>
                <el-form-item :label="$t('USER_PASSWORD')" prop="Password" :label-width="formLabelWidth">
                    <el-tooltip :content="$t('TIP_KEY_PASSWORD')" placement="right">
                        <el-input v-model="pskForm.Password" type="password" show-password class="inp-add" :placeholder="$t('PLACEHOLDER_KEY_PASSWORD')" autocomplete="off"></el-input>
                    </el-tooltip>
                </el-form-item>
                <el-form-item :label="$t('COMMENT')" prop="PSKRemarks" :label-width="formLabelWidth">
                    <el-tooltip :content="$t('TIP_REMARKS')" placement="right">
                        <el-input v-model="pskForm.PSKRemarks" type="textarea" show-word-limit maxlength="256" class="inp-add" :placeholder="$t('PLACEHOLDER_COMMENT')" autocomplete="off"></el-input>
                    </el-tooltip>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button v-no-more-click class="dialog-button" @click="handleCancel(currPage === 'mk' ? 'mkForm' : 'pskForm')">{{$t('BTN_CANCEL')}}</el-button>
                <el-button v-no-more-click class="dialog-button" type="primary" @click="handleSubmitAdd(currPage === 'mk' ? 'mkForm' : 'pskForm')">{{$t('BTN_OK')}}</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { postMK, postPSK} from '@/service/ai_vault.js'

export default {
    components: {},
    name: 'AddKey',
    props: {
        isAddKey: Boolean,
        currPage: String,
    },
    data() {
        return {
            mkForm: {
                MKName: '',
                MKUsage: '',
                Password: '',
                MKRemarks: '',
            },
            pskName: '',
            mkName: '',
            pskForm: {
                PSKName: '',
                MKName: '',
                Password: '',
                PSKRemarks: '',
            },
            formLabelWidth: '110px',
            mkRules: {
                MKName: [
                    { required: true, message: this.$t('PLACEHOLDER_KEY_NAME'), trigger: 'blur' },
                ],
                MKUsage: [
                    { required: true, message: this.$t('PLACEHOLDER_KEY_USAGE'), trigger: 'blur' },
                ],
                Password: [
                    { required: true, message: this.$t('PLACEHOLDER_MK_PASSWORD'), trigger: 'blur' },
                ],
            },
            pskRules: {
                PSKName: [
                    { required: true, message: this.$t('PLACEHOLDER_PSK_NAME'), trigger: 'blur' },
                ],
                MKName: [
                    { required: true, message: this.$t('PLACEHOLDER_MK_NAME'), trigger: 'blur' },
                ],
                Password: [
                    { required: true, message: this.$t('PLACEHOLDER_KEY_PASSWORD'), trigger: 'blur' },
                ],
            }

        };
    },
    mounted() {
    },
    watch: {
        currPage(newVal, oldVal) {
            let formName = this.currPage === 'mk' ? 'mkForm' : 'pskForm'
            if (this.$refs[formName]) {
                this.$nextTick(()=>{
                    this.$refs[formName].resetFields();
                })
            }
        }
    },
    methods: {
        handleSubmitAdd(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if(this.currPage === 'mk') {
                        postMK(this.mkForm)
                            .then(res => {
                                if (res.headers['content-disposition'] === undefined) {
                                    let reader = new FileReader();
                                    reader.onload = (e) => {
                                        let res = JSON.parse(e.target.result);
                                        if(res.status === '00002000') {
                                            this.$message.error({
                                                message: this.$t('ERR_PARAMS_CHECK_FAILED'),
                                            })
                                        } else if(res.status === '31000022') {
                                            this.$message.error({
                                              message: this.$t('ERR_SYSTEM_BUSY'),
                                            })
                                        } else if(res.status === '31000008') {
                                            this.$message.error({
                                                message: this.$t('ERR_ADD_MK'),
                                            })
                                        } else if(res.status === '31000003') {
                                            this.$message.error({
                                                message: this.$t('ERR_MAX_MK'),
                                            })
                                        } else {
                                            this.$message.error({
                                                message: this.$t('ERR_ADD'),
                                            })
                                        }
                                    }
                                    reader.readAsText(res.data)
                                } else {
                                    let blob = new Blob([res.data], {type: 'application/json'})
                                    let filename = res.headers['content-disposition'].split(';')[1].split('=')[1];
                                    let link = document.createElement('a');
                                    link.style.display = 'none';

                                    const url = window.URL || window.webkitURL || window.moxURL;
                                    link.href = url.createObjectURL(blob);
                                    link.download = filename;
                                    link.click();
                                    window.URL.revokeObjectURL(url);

                                    this.$message.success({message: this.$t('SUCCESS_ADD')})
                                    this.$emit('handleRefresh', 'mk')
                                }
                            })
                    } else {
                        this.mkName = this.pskForm.MKName
                        this.pskName = this.pskForm.PSKName
                        postPSK(this.pskForm)
                            .then(res => {
                                if(res.data.status === '00000000') {
                                    let blob = new Blob([res.data.data.PSK], {type: 'application/none'})
                                    let filename = "aiguard-preshared-key"
                                    let link = document.createElement('a');
                                    link.style.display = 'none';
                                    const url = window.URL || window.webkitURL || window.moxURL;
                                    link.href = url.createObjectURL(blob);
                                    link.download = filename;
                                    link.click();
                                    window.URL.revokeObjectURL(url);
                                    this.$emit('handleRefresh', 'psk')

                                } else if(res.data.status === '31000009') {
                                    this.$message.error({
                                        message: this.$t('ERR_ADD_PSK'),
                                    })
                                } else if(res.data.status === '31000010') {
                                    this.$message.error({
                                        message: this.$t('ERR_MAX_PSK'),
                                   })
                                } else if(res.data.status === '31000004') {
                                    this.$message.error({
                                        message: this.$t('ERR_MK_AREADY_BIND'),
                                    })
                                } else if(res.data.status === '00002000') {
                                    this.$message.error({
                                        message: this.$t('ERR_PARAMS_CHECK_FAILED'),
                                    })
                                } else if(res.data.status === '31000011') {
                                    this.$message.error({
                                        message: this.$t('ERR_ADD_PSK_MK_NOT_EXIST'),
                                    })
                                } else if(res.data.status === '31000022') {
                                  this.$message.error({
                                    message: this.$t('ERR_SYSTEM_BUSY'),
                                  })
                                } else {
                                    this.$message.error({
                                        message: this.$t('ERR_ADD'),
                                    })
                                }
                            })
                    }
                    this.handleCancel(this.currPage === 'mk' ? 'mkForm' : 'pskForm')
                } else {
                    return false
                }
            })
        },
        handleCancel(formName) {
            this.$nextTick(()=>{
                this.$refs[formName].resetFields();
                this.$emit('handleCancelAdd')
            })
        },
        handleClose() {
            this.$emit('handleCancelAdd')
        },
    }
}
</script>

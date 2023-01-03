<template>
  <div>
    <el-dialog
        :title=" $t('ADD_CERT')"
        :visible.sync="isAddCert"
        :close-on-click-modal="false"
        :before-close="handleClose"
        width="30%"
        :modal="false"
    >
      <div  style="background: rgba(249,118,17,0.2);border-radius: 2px;display: flex; padding-bottom: 8px; padding-top: 8px; margin-bottom: 24px">
        <div style="margin-left: 8px"><img src="@/assets/icon/alarm-orange.svg"></div>
        <div style="margin-left: 8px">{{ $t('ADD_CERT_TIP')}}</div>
      </div>

      <el-form :model="certForm" :rules="certRules" ref="certForm" key="CertKey">
        <el-form-item :label="$t('CERT_COMMONNAME')" prop="CommonName" :label-width="formLabelWidth">
          <el-tooltip :content="$t('TIP_COMMON')" placement="right">
            <el-input v-model="certForm.CommonName" class="inp-add" :placeholder="$t('PLACEHOLDER_CERT_COMMONNAME')" autocomplete="off"></el-input>
          </el-tooltip>
        </el-form-item>
        <el-form-item :label="$t('CFS_PASSWORD')" prop="CfsPassword" :label-width="formLabelWidth">
          <el-tooltip :content="$t('TIP_KEY_PASSWORD')" placement="right">
            <el-input v-model="certForm.CfsPassword" type="password" show-password class="inp-add" :placeholder="$t('PLACEHOLDER_CERT_KEYWORD')" autocomplete="off"></el-input>
          </el-tooltip>
        </el-form-item>
        <el-form-item :label="$t('CERT_ORGANIZATION_NAME')" prop="OrganizationName"  :label-width="formLabelWidth">
          <el-tooltip :content="$t('TIP_COMMON')" placement="right">
            <el-input v-model="certForm.OrganizationName" class="inp-add" :placeholder="$t('PLACEHOLDER_CERT_ORGANIZATION')" autocomplete="off"></el-input>
          </el-tooltip>
        </el-form-item>
        <el-form-item :label="$t('CERT_UNIT_NAME')" prop="OrganizationalUnitName"  :label-width="formLabelWidth">
          <el-tooltip :content="$t('TIP_COMMON')" placement="right">
            <el-input v-model="certForm.OrganizationalUnitName" class="inp-add" :placeholder="$t('PLACEHOLDER_CERT_UNIT')" autocomplete="off"></el-input>
          </el-tooltip>
        </el-form-item>
        <el-row>
          <el-form-item :label="$t('CERT_LOCATION')"  :label-width="formLabelWidth" >
            <el-col :span="7">
              <el-form-item prop="CountryName">
                <el-tooltip :content="$t('TIP_LOCATION')" placement="right">
                  <el-input v-model="certForm.CountryName" class="inp-add" :placeholder="$t('PLACEHOLDER_CERT_COUNTRY')"
                            autocomplete="off"></el-input>
                </el-tooltip>
              </el-form-item>
            </el-col>
            <el-col class="line" :span="1">-</el-col>
            <el-col :span="7">
              <el-form-item prop="StateOrProvinceName">
                <el-tooltip :content="$t('TIP_COMMON')" placement="right">
                  <el-input v-model="certForm.StateOrProvinceName" class="inp-add" :placeholder="$t('PLACEHOLDER_CERT_PROVINCE')"
                            autocomplete="off"></el-input>
                </el-tooltip>
              </el-form-item>
            </el-col>
            <el-col class="line" :span="1">-</el-col>
            <el-col :span="7">
              <el-form-item prop="LocalityName">
                <el-tooltip :content="$t('TIP_COMMON')" placement="right">
                  <el-input v-model="certForm.LocalityName" class="inp-add" :placeholder="$t('PLACEHOLDER_CERT_CITY')"
                            autocomplete="off"></el-input>
                </el-tooltip>
              </el-form-item>
            </el-col>
          </el-form-item>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
                <el-button v-no-more-click class="dialog-button" @click="handleCancel('certForm')">{{$t('BTN_CANCEL')}}</el-button>
                <el-button v-no-more-click class="dialog-button" type="primary" @click="handleSubmitAdd('certForm')">{{$t('BTN_OK')}}</el-button>
            </span>
    </el-dialog>
  </div>
</template>

<script>
import { postCert } from '@/service/ai_vault.js'

export default {
  components: {},
  name: 'AddCert',
  props: {
    isAddCert: Boolean,
    currPage: String,
  },
  data() {
    return {
      certForm: {
        CommonName: '',
        CfsPassword: '',
        OrganizationName: '',
        OrganizationalUnitName: '',
        CountryName: '',
        StateOrProvinceName: '',
        LocalityName: '',
      },
      certName: '',
      formLabelWidth: '110px',
      certRules: {
        CommonName: [
          { required: true, message: this.$t('PLACEHOLDER_CERT_COMMONNAME'), trigger: 'blur' },
        ],
        CfsPassword: [
          { required: true,min: 40, max :64,message: this.$t('PLACEHOLDER_CERT_KEYWORD'), trigger: 'blur' },
        ],
        OrganizationName: [
          { required: false,max:64, message: this.$t('PLACEHOLDER_CERT_ORGANIZATION'), trigger: 'blur' },
        ],
        OrganizationalUnitName: [
          { required: false,max :64, message: this.$t('PLACEHOLDER_CERT_UNIT'), trigger: 'blur' },
        ],
        CountryName: [
          { required: false, max :2, message: this.$t('PLACEHOLDER_CERT_COUNTRY'), trigger: 'blur' },
        ],
        StateOrProvinceName: [
          { required: false,max :2, message: this.$t('PLACEHOLDER_CERT_PROVINCE'), trigger: 'blur' },
        ],
        LocalityName: [
          { required: false,max :2, message: this.$t('PLACEHOLDER_CERT_CITY'), trigger: 'blur' },
        ],
      },
    };
  },
  mounted() {
  },
  watch: {
    currPage(newVal, oldVal) {
      let formName = 'certForm'
      if (this.$refs[formName]) {
        this.$nextTick(() => {
          this.$refs[formName].resetFields();
        })
      }
    }
  },
  methods: {
    handleSubmitAdd(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if(true) {
            postCert(this.certForm,{})
                .then(res => {
                  if (res.headers['content-disposition'] === undefined) {
                    let reader = new FileReader();
                    reader.onload = (e) => {
                      let res =  JSON.parse(e.target.result);
                      if(res.status === '00002000') {
                        this.$message.error({
                          message: this.$t('ERR_PARAMS_CHECK_FAILED'),
                        })
                      } else if(res.status === '31000022') {
                        this.$message.error({
                          message: this.$t('ERR_SYSTEM_BUSY'),
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
                    this.handleCancel( 'certForm')
                    this.$message.success({message: this.$t('SUCCESS_APPLY')})
                    this.$emit('handleRefresh', 'mk')
                  }
                })
          }
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

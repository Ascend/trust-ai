<template>
  <div class="main">
    <div class="info-block">
      <el-row :gutter="20">
          <el-col :span="8" class="info-col">
              <img class="info-img" src="@/assets/user/version.png" />
              <div class="info-subitem">
                  <div class="info-subitem-title">{{$t('VERSION')}}</div>
                  <span class="info-subitem-text">{{ version }}</span>
              </div>
          </el-col>
          <el-col :span="8" class="info-col">
              <img class="info-img" src="@/assets/user/healthStatus.png" />
              <div class="info-subitem">
                  <div class="info-subitem-title">{{$t('HEALTH_STATUS')}}</div>
                  <span class="info-subitem-text">{{ healthStatus }}</span>
              </div>
          </el-col>
      </el-row>
    </div>
    
    <el-table
      :data="tableData"
      :span-method="objectSpanMethod"
      style="width: 100%; margin-top: 20px"
      :cell-style="{ textAlign: 'center', border: '0.5px solid rgb(123, 143, 175, 0.5)', padding: '10px 0', }"
      :header-cell-style="{ textAlign: 'center', padding: '10px 0', }"
      :empty-text="$t('EMPTY_TEXT')"
    >
      <el-table-column prop="CertType" :label="$t('COLUMN_CERT_TYPE')"></el-table-column>
      <el-table-column prop="CertValidDate" :label="$t('COLUMN_CERT_VALID_DATE')"></el-table-column>
      <el-table-column prop="CertAlarm" :label="$t('COLUMN_CERT_ALARM')"></el-table-column>
      <el-table-column prop="CrlStatus" :label="$t('COLUMN_CRL_STATUS')"></el-table-column>
    </el-table>

    <div class="home-operation">
      <el-upload
        class="upload-demo"
        action="/datamanager/v1/import"
        :file-list="fileList"
        style="display: inline-block;"
        :before-upload="handleBeforeUpload"
        :show-file-list="false"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        >
        <el-button style="margin-left: 10px;" type="primary">{{ $t('BUTTON_UPLOAD') }}</el-button>
      </el-upload>

      <el-button 
        type="primary" 
        plain 
        style="margin-left: 10px;"
        @click="handleDownload"
      >
        {{ $t('BUTTON_DOWNLOAD') }}
      </el-button>
    </div>
  </div>
</template>

<script>
import { fetchVersion, fetchHealthStatus, fetchCertStatus, exportFile } from '@/service/home.js'

export default {
  name: 'home',
  data () {
    return {
      username: '',
      password: '',
      version: '',
      tableData: [],
      healthStatus: '',
      spanArr: [],
      position: 0,
      fileList: [],
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    queryVersion() {
      fetchVersion()
        .then(res => {
          if(res.data.status === '31000022') {
            let timerVersion = setTimeout(() => {
              this.queryVersion()
              clearTimeout(timerVersion)
            }, 1000);
          }
            this.version = res.data.data.version.split('_')[0]
        })
    },
    queryHealth() {
      fetchHealthStatus()
        .then(res => {
          if(res.data.status === '31000022') {
            let timerHealth = setTimeout(() => {
              this.queryHealth()
              clearTimeout(timerHealth)
            }, 1000);
          }
            this.healthStatus = res.data.msg === 'ok' ? '健康' : '不健康'
        })
    },
    queryCert() {
      fetchCertStatus()
        .then(res => {
          if(res.data.status === '31000022') {
            let timerCert = setTimeout(() => {
              this.queryCert()
              clearTimeout(timerCert)
            }, 1000);
          }
            this.tableData = res.data.data
            this.handleSpan()
        })
    },
    fetchData() {
      this.queryVersion()
      this.queryHealth()
      this.queryCert()      
    },
    handleSpan() {
      let mgmtArr = this.tableData.filter(item => item.CertType === 'MGMT')
      let svcArr = this.tableData.filter(item => item.CertType !== 'MGMT')
      this.tableData = mgmtArr.concat(svcArr)

      this.tableData.forEach((item, index) => {
          item.CertType = {'MGMT': '管理面' , 'SVC': '服务面'}[item.CertType]
          item.CertAlarm = item.CertAlarm === '' ? '正常' : '不正常'
          item.CrlStatus = item.CrlStatus === 'No CRL certificate has been imported.' ? '未导入' : '已导入'
          if(index === 0) {
              this.spanArr.push(1)
              this.position = 0
          } else {
              if(this.tableData[index].CertType === this.tableData[index - 1].CertType) {
                  this.spanArr[this.position] += 1;
                  this.spanArr.push(0)
              } else {
                  this.spanArr.push(1)
                  this.position = index
              }
          }
      })
    },
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      if (columnIndex === 0) {
          const _row = this.spanArr[rowIndex]
          const _col = _row > 0 ? 1 : 0;
          return {
              rowspan: _row,
              colspan: _col
          }
      }
    },    
    handleBeforeUpload(file) {
      const isZip = file.type.indexOf('zip') > -1;
      const isLt50M = file.size / 1024 / 1024 <= 50;

      if (!isZip) {
        this.$message.error(this.$t('ERR_UPLOAD_FILE_TYPE'));
      }
      if (!isLt50M) {
        this.$message.error(this.$t('ERR_UPLOAD_FILE_SIZE'));
      }
      return isZip && isLt50M;
    },
    handleDownload() {
      exportFile()
        .then(res => {
          if (res.headers['content-disposition'] === undefined) {
            let reader = new FileReader();
            reader.onload = (e) => {
                let res = JSON.parse(e.target.result);
                if(res.status === '41000002') {
                    this.$message.error({
                        message: this.$t('ERR_DOWNLOAD'),
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
          }
        })
    },
    handleUploadSuccess(response, file, fileList) {
      if(response.status === "00000000") {
        this.$message.success({message: this.$t('SUCCESS_UPLOAD')})
      } else {
        this.$message.warning({message: this.$t('ERR_UPLOAD')})
      }
    },
    handleUploadError(err, file, fileList) {
      this.$message.warning({message: this.$t('ERR_UPLOAD')})
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home-operation {
  margin-top: 20px;
}
  .info-block {
      background-color: #1f2329;
      height: 64px;
      border-radius: 4px;
      padding: 16px 24px;
      margin-top: 10px;
  }
  
  .info-col {
      display: flex;
      vertical-align: center;
  }
  .info-subitem {
      display: inline-block;
  }
  
  .info-subitem-title {
      margin-left: 10px;
      font-size: 14px;
      color: #6A6A6A;
  }
  
  .info-subitem-text {
      margin-left: 10px;
      font-size: 32px;
      color: #6A6A6A;
  }
  </style>
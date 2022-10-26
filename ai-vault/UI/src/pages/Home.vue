<template>
  <div class="home">
    <div class="left">
      <div class="left-box first-left">
        <div class="left-name">{{ $t("USER_AMOUNT") }}</div>
        <div class="left-num">{{ useramount }}</div>
      </div>
      <div class="left-box">
        <div class="left-name">{{ $t("SYS_DATA_SIZE") }}</div>
        <div class="left-num">{{ datasize }}</div>
      </div>
    </div>
    <div class="right">
      <div class="right-box right-top">

        <div class="sbutton">
          <div class="title">{{ $t("TOOL_INFO") }}</div>
        </div>
        <div class="top-button">
            <el-button type="text" icon="add-icon" style="color:#D3DCE9">{{ $t('BUTTON_UPLOAD') }}</el-button>
            <el-button type="text" icon="add-icon" style="color:#D3DCE9">{{ $t('BUTTON_DOWNLOAD') }}</el-button>
        </div>
        <div class="info-block">
          <div class="right_name">{{ $t("VERSION") }}</div>
          <div class="right_info">{{ version }}</div>
        </div>
        <div class="info-block">
          <div class="right_name">{{ $t("HEALTH_STATUS") }}</div>
          <div class="right_info">{{ healthStatus }}</div>
        </div>
      </div>
      <div class="right-box">
        <div class="title">{{ $t("CERT_INFO") }}</div>
        <div class="info-block">
          <div class="right_name">{{ $t("COLUMN_CERT_TYPE") }}</div>
          <div class="right_info">{{ tableData[0].CertType }}</div>
        </div>
        <div class="info-block">
          <div class="right_name">{{ $t("COLUMN_CERT_VALID_DATE") }}</div>
          <div class="right_info">{{ tableData[0].CertValidDate }}</div>
        </div>
        <div class="info-block">
          <div class="right_name">{{ $t("COLUMN_CERT_ALARM") }}</div>
          <div class="right_info">{{ tableData[0].CertAlarm }}</div>
        </div>
        <div class="info-block">
          <div class="right_name">{{ $t("COLUMN_CRL_STATUS") }}</div>
          <div class="right_info">{{ tableData[0].CrlStatus }}</div>
        </div>
      </div>
      <div class="right-box">
        <div class="title">{{ $t("CERT_INFO") }}</div>
        <div class="info-block">
          <div class="right_name">{{ $t("COLUMN_CERT_TYPE") }}</div>
          <div class="right_info">{{ tableData[1].CertType }}</div>
        </div>
        <div class="info-block">
          <div class="right_name">{{ $t("COLUMN_CERT_VALID_DATE") }}</div>
          <div class="right_info">{{ tableData[1].CertValidDate }}</div>
        </div>
        <div class="info-block">
          <div class="right_name">{{ $t("COLUMN_CERT_ALARM") }}</div>
          <div class="right_info">{{ tableData[1].CertAlarm }}</div>
        </div>
        <div class="info-block">
          <div class="right_name">{{ $t("COLUMN_CRL_STATUS") }}</div>
          <div class="right_info">{{ tableData[1].CrlStatus }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchDataSize, fetchVersion, fetchHealthStatus, fetchCertStatus, exportFile } from '@/service/home.js'
import {fetchUser} from '@/service/user.js'

export default {
  name: 'home',
  data () {
    return {
      useramount: 0,
      datasize: 0,
      version: '',
      tableData: [],
      healthStatus: '',
      spanArr: [],
      position: 0,
      fileList: [],
    }
  },
  mounted() {
    this.queryData()
  },
  methods: {
    queryData() {
      fetchUser({})
        .then(res => {
              this.useramount = res.data.data.total
          })
      // fetchDataSize()
      //   .then(res => {
      //     this.datasize = res.data.data.size
      //   })
      fetchVersion()
        .then(resVersion => {
          if(resVersion.data.status === '31000022') {
            let timerVersion = setTimeout(() => {
              this.queryData()
              clearTimeout(timerVersion)
            }, 1000);
          }

          fetchHealthStatus()
            .then(resHealth => {
              if(resHealth.data.status === '31000022') {
                let timerHealth = setTimeout(() => {
                  this.queryData()
                  clearTimeout(timerHealth)
                }, 1000);
              }

              fetchCertStatus()
                .then(resCert => {
                  if(resCert.data.status === '31000022') {
                    let timerCert = setTimeout(() => {
                      this.queryData()
                      clearTimeout(timerCert)
                    }, 1000);
                  }
                    this.tableData = resCert.data.data
                    this.handleSpan()
                    this.healthStatus = resHealth.data.msg === 'ok' ? '健康' : '不健康'
                    this.version = resVersion.data.data.version.split('_')[0]
                })
            })
        })
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
.home{
  padding: 64px 24px 24px;
  display: flex;
  flex-direction: row;
  overflow: auto;
}


.left {
  flex-grow: 1;
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin-top: 6px;
  min-width: 855px;
}
.left-box {
  padding: 0 57px;
  height: 108px;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}
.first-left:before {
  content: '';
  width: 1px;
  height: 40px;
  position: absolute;
  right: 0;
  top: 50%;
  margin-top: -20px;
  background: #8D98AA;
}
.left-name {
  font-size: 21px;
  color: #8D98AA;
  line-height: 30px;
  font-weight: 400;
  letter-spacing: 0;
  text-align: center;
}
.left-num {
  font-size: 54px;
  color: #FFFFFF;
  line-height: 80px;
  font-weight: 400;
  text-align: center;
  letter-spacing: 0;
}

.right {
  width: 348px;
  min-width: 348px;
  letter-spacing: 0;
  font-size: 12px;
  color: #8D98AA;
}


.title {
  font-size: 16px;
  align-items: center;
  color: #FFFFFE;
  letter-spacing: 0;
  line-height: 24px;
  font-weight: 400;
}

.top-button {
  align-items: center;
  font-size: 12px;
  line-height: 16px;
  font-weight: 500;
}

.right_name {
  font-size: 12px;
  line-height: 20px;
  font-weight: 400;
  letter-spacing: 0;
  color: #8D98AA;
}

.right_info {
  font-size: 20px;
  line-height: 30px;
  letter-spacing: 0;
  font-weight: 400;
  color: #FFFFFE;
}

.right-box {
  background: #2A2F37;
  border-radius: 6px;
  padding: 24px;
  margin-bottom: 16px;
}

.info-block {
  margin-top: 8px;
  margin-bottom: 8px;
}

</style>

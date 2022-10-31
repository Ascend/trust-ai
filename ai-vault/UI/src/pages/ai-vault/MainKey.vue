<template>
    <div>
        <el-button
            v-no-more-click
            type="primary"
            icon="el-icon-circle-plus-outline"
            class="btn-add"
            @click="handleAddMainKey"
        >
            {{ $t('BUTTON_ADD') }}
       </el-button>
        <div class="tab-main-operation">
            <el-input
                type="text"
                prefix-icon="el-icon-search"
                v-model="queryMainKeyParams.mkName"
                class="input-search"
                :placeholder="$t('PLACEHOLDER_INPUT')"
                clearable
                @keyup.enter.native="fetchData"
            ></el-input>
            <el-button
                v-no-more-click
                icon="el-icon-refresh"
                class="button-refresh"
                @click="fetchData"
            ></el-button>
        </div>
        <el-table
            :data="tableData"
            style="width: 100%"
            class="table-main-key"
            @sort-change="handleSortMKTable"
            max-height="600"
            :highlight-current-row="true"
            :cell-style="{ textAlign: 'center', padding: '10px 0', }"
            :header-cell-style="{ textAlign: 'center', padding: '10px 0', }"
            :empty-text="$t('EMPTY_TEXT')"
        >
            <el-table-column prop="MKName" :label="$t('COLUMN_NAME')" sortable="custom"></el-table-column>
            <el-table-column prop="MKUsage" :label="$t('COLUMN_KEY_USAGE')"></el-table-column>
            <el-table-column prop="CreatedAt" :label="$t('COLUMN_CREATE_TIME')" sortable="custom"></el-table-column>
            <el-table-column prop="MKRemarks" :label="$t('COLUMN_REMARKS')"></el-table-column>
            <el-table-column prop="operation" :label="$t('COLUMN_OPERATION')">
                <template slot-scope="scope">
                    <el-button v-no-more-click @click="handleConfirmDelete(scope.row)" type="text" plain size="small">
                        {{ $t('OPERATION_DELETE') }}
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog
            :title="$t('CONFIRM_DELETE')"
            :visible.sync="isDelete"
            width="28%"
            :close-on-click-modal="false"
            :modal="false"
        >   <div style="display: flex;">
                <div style="margin-left: 16px; margin-right: 16px"><img src="@/assets/icon/warn.svg"></div>
                {{$t('CONFIRM_DELETE_KEY_TIP')}}{{$t('CONFIRM_DELETE_TIP')}} {{ selectedRow.MKName }}?
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button v-no-more-click class="dialog-button" @click="isDelete = false">{{$t('BTN_CANCEL')}}</el-button>
                <el-button v-no-more-click class="dialog-button" type="primary" @click="handleDelete">{{$t('BTN_OK')}}</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { fetchMainKey, deleteMK } from '@/service/ai_vaul'
import moment from 'moment'

export default {
    components: {},
    name: 'MainKey',
    props: {
        currPage: String,
        isRefresh: Boolean,
    },
    data() {
        return {
            tableData: [],
            queryMainKeyParams: {
                mkName: '',
                sortBy: 'CreateTime',
                sortMode: 'desc',
            },
            isDelete: false,
            selectedRow: {},
        };
    },
    mounted() {
        this.fetchData()
    },
    watch: {
        currPage(newPage, oldPage) {
            if(newPage === 'mk') {
                this.fetchData()
            }
        },
        isRefresh(newValue, oldValue){
            this.fetchData()
        },
    },
    methods: {
        fetchData() {
            let params = {
                PageSize: 10,
                SortBy: this.queryMainKeyParams.sortBy,
                SortMode: this.queryMainKeyParams.sortMode,
            }

            if (this.queryMainKeyParams.mkName.length > 0) {
                params.MKName =  this.queryMainKeyParams.mkName
            }

            fetchMainKey(params)
              .then(res => {
                const format = 'YYYY-MM-DD HH:mm:ss';
                res.data.data.data.forEach(item => {
                    item.CreatedAt = moment(item.CreatedAt).format(format)
                })
                this.tableData = res.data.data.data
              })
        },
        handleAddMainKey() {
            this.$emit('handleAddMK')
        },
        handleSortMKTable({column, prop, order}) {
            this.queryMainKeyParams.sortBy = prop === 'CreatedAt' ? 'CreateTime' : prop
            this.queryMainKeyParams.sortMode = {'ascending': 'asc', 'descending': 'desc'}[order]
            this.fetchData()
        },
        handleConfirmDelete(row) {
            this.selectedRow = row
            this.isDelete = true
        },
        handleDelete(){
            deleteMK(this.selectedRow.MKName)
                .then(res => {
                    if(res.data.status === '00000000') {
                        this.$message.success({
                            message: this.$t('SUCCESS_DELETE'),
                        })
                        this.isDelete = false
                        this.fetchData()
                    } else if(res.data.status === '31000022') {
                        this.$message.error({
                            message: this.$t('ERR_SYSTEM_BUSY'),
                        })
                        this.isDelete = false
                    } else if(res.data.status === '31000005') {
                        this.$message.error({
                            message: this.$t('ERR_DELETE') + '。' + this.$t('ERR_DELETE_MK'),
                        })
                        this.isDelete = false
                    } else {
                        this.$message.error({
                          message: this.$t('ERR_DELETE') + '。',
                      })
                        this.isDelete = false
                    }
                })
                .catch(err => {
                    this.isDelete = false
                })
        }
    }
}
</script>
<style scoped>
.tab-main-operation {
    display: flex;
    align-items: center;
    float: right;
}

.btn-add {
  float: left;
  margin-left: 10px;
  background: #0077FF;
  border-radius: 2px;
  color: #FFFFFF;
}

.input-search {
    width: 280px;
    margin-left: 10px;
}

.button-refresh {
    margin-left: 10px;
}

.table-main-key {
    margin-top: 70px;
}

</style>

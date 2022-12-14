webpackJsonp([2],{"fT/Z":function(e,t){},sNDf:function(e,t,s){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a=s("y5xs"),r={components:{UserManage:s("txoQ").a},name:"user",data:function(){var e=this;return{abortController:new AbortController,useramount:0,userData:[],userPagination:{total:10},sortParams:{SortBy:"UserID",SortMode:"asc"},pageParams:{CurrentPage:1,PageSize:10},resetPswForm:{UserName:"",NewPassword:"",NewPasswordConfirm:""},formLabelWidth:"100px",selectedRow:{},isDelorReset:!1,indexOperation:"",isAddUser:!1,UserName:"",resetPswRules:{NewPassword:[{required:!0,message:this.$t("PLACEHOLDER_NEW_PASSWORD"),trigger:"blur"}],NewPasswordConfirm:[{required:!0,message:this.$t("PLACEHOLDER_CONFIRM_PASSWORD"),trigger:"blur"},{validator:function(t,s,a){s!==e.resetPswForm.NewPassword?a(new Error(e.$t("ERR_CANNOT_CONFIRM_NEW_PASSWORD"))):a()},trigger:"blur"}]},tableHeight:window.innerHeight-330}},watch:{isDelorReset:function(e,t){var s=this;"resetPWD"===this.indexOperation&&this.$nextTick(function(){s.$refs.resetPswForm.resetFields()})}},mounted:function(){this.fetchUserList()},beforeDestroy:function(){this.abortController.abort()},methods:{fetchUserList:function(){var e=this,t={PageSize:10,CurrentPage:this.pageParams.CurrentPage,SortBy:this.sortParams.SortBy,SortMode:this.sortParams.SortMode};this.UserName.length>0&&(t.UserName=this.UserName),Object(a.d)(t).then(function(t){t.data.data.users.forEach(function(e){e.Role={1:"管理员",4:"普通用户"}[e.RoleID]}),e.userData=t.data.data.users,e.userPagination.total=t.data.data.total}),this.handleGetUserAmount()},handleConfirmDelete:function(e){this.selectedRow=e,this.indexOperation="delUser",this.isDelorReset=!0},handleConfirmReset:function(e){this.selectedRow=e,this.indexOperation="resetPWD",this.isDelorReset=!0},handleSubmitResetPassword:function(){var e=this;this.$refs.resetPswForm.validate(function(t){t&&(e.resetPswForm.UserName=e.selectedRow.UserName,Object(a.e)(e.resetPswForm).then(function(t){"00000000"===t.data.status?(e.$message.success({message:e.$t("SUCCESS_RESET_PASSWORD")}),e.isDelorReset=!1,e.fetchUserList()):"00002000"===t.data.status?e.$message.error({message:e.$t("ERR_PARAMS_CHECK_FAILED")}):e.$message.error({message:e.$t("ERR_RESET_PASSWORD")})}).catch(function(t){e.isDelorReset=!1}))})},handleDelete:function(){var e=this;Object(a.c)(this.selectedRow.UserName).then(function(t){"00000000"===t.data.status?(e.$message.success({message:e.$t("SUCCESS_DELETE")}),e.isDelorReset=!1,e.fetchUserList()):"21000001"===t.data.status?e.$message.error({message:e.$t("ERR_DELETE")+"。"+e.$t("ERR_CONNECT_AIVAULT")}):"21000009"===t.data.status?e.$message.error({message:e.$t("ERR_DELETE")+"。"+e.$t("ERR_DELETE_USER")}):e.$message.error({message:e.$t("ERR_DELETE")+"。"})}).catch(function(t){e.isDelorReset=!1})},handleConfirmAddUser:function(){this.isAddUser=!0},handleCancel:function(){this.isAddUser=!1,this.fetchUserList()},handleSizeChange:function(e){this.pageParams.PageSize=e,this.fetchUserList()},handleCurrentChange:function(e){this.pageParams.CurrentPage=e,this.fetchUserList()},handleSearch:function(){this.pageParams.CurrentPage=1,this.fetchUserList()},handleClear:function(){this.pageParams.CurrentPage=1,this.fetchUserList()},handleSortUserTable:function(e){e.column;var t=e.prop,s=e.order;this.sortParams.SortBy="UserID"===t?"UserID":t,this.sortParams.SortMode={ascending:"asc",descending:"desc"}[s],this.fetchUserList()},handleGetUserAmount:function(){var e=this;Object(a.d)({}).then(function(t){e.useramount=t.data.data.total})}}},n={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticStyle:{"margin-bottom":"20px",overflow:"auto"}},[a("div",{staticClass:"user-amount"},[e._v("\n        "+e._s(e.$t("NAV_USER"))+"\n    ")]),e._v(" "),a("div",{staticClass:"menu"},[a("div",{staticClass:"name-wrapper"},[a("img",{staticClass:"back-up",attrs:{src:s("mxiF")}}),e._v(" "),a("div",{staticClass:"user-margin"},[e._v(e._s(e.$t("USER_AMOUNT")))]),e._v(" "),a("div",{staticClass:"num"},[e._v(" "+e._s(e.useramount)+" ")])])]),e._v(" "),a("div",{staticStyle:{"margin-top":"16px"}},[a("el-button",{directives:[{name:"no-more-click",rawName:"v-no-more-click"}],staticClass:"button-add",attrs:{type:"primary",icon:"el-icon-circle-plus-outline"},on:{click:e.handleConfirmAddUser}},[e._v("\n              "+e._s(e.$t("BUTTON_ADD_USER"))+"\n        ")]),e._v(" "),a("div",{staticClass:"user-operation"},[a("el-input",{staticClass:"input-search",attrs:{type:"text","prefix-icon":"el-icon-search",placeholder:e.$t("PLACEHOLDER_INPUT"),clearable:""},on:{clear:e.handleClear},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleSearch.apply(null,arguments)}},model:{value:e.UserName,callback:function(t){e.UserName=t},expression:"UserName"}}),e._v(" "),a("el-button",{directives:[{name:"no-more-click",rawName:"v-no-more-click"}],staticClass:"button-refresh",attrs:{icon:"el-icon-refresh"},on:{click:e.handleSearch}})],1),e._v(" "),a("div",{staticStyle:{background:"#1f2329"}},[a("div",{staticStyle:{padding:"0 24px"}},[a("el-table",{staticStyle:{width:"100%"},attrs:{data:e.userData,"highlight-current-row":!0,"cell-style":{textAlign:"center",padding:"10px 0"},"header-cell-style":{textAlign:"center",padding:"10px 0"},"empty-text":e.$t("EMPTY_TEXT"),"max-height":"600",height:e.tableHeight},on:{"sort-change":e.handleSortUserTable}},[a("el-table-column",{attrs:{prop:"UserID",label:e.$t("COLUMN_USER_ID"),sortable:"custom"}}),e._v(" "),a("el-table-column",{attrs:{prop:"UserName",label:e.$t("COLUMN_USER_NAME")}}),e._v(" "),a("el-table-column",{attrs:{prop:"Role",label:e.$t("COLUMN_USER_TYPE")}}),e._v(" "),a("el-table-column",{attrs:{prop:"CreateTime",label:e.$t("COLUMN_CREATE_TIME"),sortable:"custom"}}),e._v(" "),a("el-table-column",{attrs:{prop:"operation",label:e.$t("COLUMN_OPERATION"),width:"240"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{attrs:{disabled:1===t.row.RoleID,type:"text",size:"small"},on:{click:function(s){return e.handleConfirmReset(t.row)}}},[e._v("\n                        "+e._s(e.$t("RESET_PASSWORD"))+"\n                    ")]),e._v(" "),a("el-button",{attrs:{disabled:1===t.row.RoleID,type:"text",size:"small"},on:{click:function(s){return e.handleConfirmDelete(t.row)}}},[e._v("\n                        "+e._s(e.$t("OPERATION_DELETE"))+"\n                    ")])]}}])})],1)],1),e._v(" "),a("el-pagination",{staticStyle:{"padding-bottom":"24px","margin-bottom":"24px","margin-left":"24px"},attrs:{"current-page":e.pageParams.CurrentPage,"page-size":e.pageParams.PageSize,total:e.userPagination.total,layout:"total, prev, pager, next, jumper"},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange,"update:currentPage":function(t){return e.$set(e.pageParams,"CurrentPage",t)},"update:current-page":function(t){return e.$set(e.pageParams,"CurrentPage",t)}}})],1)],1),e._v(" "),a("el-dialog",{attrs:{title:"resetPWD"===e.indexOperation?e.$t("RESET_PASSWORD"):e.$t("CONFIRM_DELETE"),visible:e.isDelorReset,width:"28%","close-on-click-modal":!1,modal:!1},on:{"update:visible":function(t){e.isDelorReset=t}}},["resetPWD"===e.indexOperation?a("el-form",{ref:"resetPswForm",attrs:{model:e.resetPswForm,rules:e.resetPswRules}},[a("el-form-item",{attrs:{label:e.$t("NEW_PSW"),prop:"NewPassword","label-width":e.formLabelWidth}},[a("el-tooltip",{attrs:{content:e.$t("TIP_PASSWORD"),placement:"right"}},[a("el-input",{staticClass:"input-psw",attrs:{type:"password",placeholder:e.$t("PLACEHOLDER_NEW_PASSWORD"),autocomplete:"off"},model:{value:e.resetPswForm.NewPassword,callback:function(t){e.$set(e.resetPswForm,"NewPassword",t)},expression:"resetPswForm.NewPassword"}})],1)],1),e._v(" "),a("el-form-item",{attrs:{label:e.$t("CONFIRM_PSW"),prop:"NewPasswordConfirm","label-width":e.formLabelWidth}},[a("el-tooltip",{attrs:{content:e.$t("TIP_PASSWORD"),placement:"right"}},[a("el-input",{staticClass:"input-psw",attrs:{type:"password",placeholder:e.$t("PLACEHOLDER_CONFIRM_PASSWORD"),autocomplete:"off"},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleSubmitResetPassword()}},model:{value:e.resetPswForm.NewPasswordConfirm,callback:function(t){e.$set(e.resetPswForm,"NewPasswordConfirm",t)},expression:"resetPswForm.NewPasswordConfirm"}})],1)],1)],1):a("div",{staticClass:"dialog-tip"},[a("div",{staticStyle:{"margin-left":"16px","margin-right":"16px"}},[a("img",{attrs:{src:s("77VW")}})]),e._v("\n            "+e._s(e.$t("CONFIRM_DELETE_TIP"))+": "+e._s(e.selectedRow.UserName)+"?\n        ")]),e._v(" "),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{directives:[{name:"no-more-click",rawName:"v-no-more-click"}],staticClass:"dialog-button",on:{click:function(t){e.isDelorReset=!1}}},[e._v(e._s(e.$t("BTN_CANCEL")))]),e._v(" "),a("el-button",{directives:[{name:"no-more-click",rawName:"v-no-more-click"}],staticClass:"dialog-button",attrs:{type:"primary"},on:{click:function(t){"resetPWD"===e.indexOperation?e.handleSubmitResetPassword():e.handleDelete()}}},[e._v(e._s(e.$t("BTN_OK")))])],1)],1),e._v(" "),a("user-manage",{attrs:{isShow:e.isAddUser,currOperation:"addUser"},on:{handleCancel:e.handleCancel}})],1)},staticRenderFns:[]};var o=s("VU/8")(r,n,!1,function(e){s("fT/Z")},"data-v-ab2fe3ba",null);t.default=o.exports}});
//# sourceMappingURL=2.5a5041caa9460ced4f2d.js.map
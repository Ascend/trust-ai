webpackJsonp([2],{sNDf:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=a("y5xs"),n={components:{UserManage:a("txoQ").a},name:"user",data:function(){return{userData:[],userPagination:{total:0},userParams:{CurrentPage:1,PageSize:10},isDelete:!1,selectedRow:{},isAddUser:!1,UserName:""}},mounted:function(){this.fetchUserList()},methods:{fetchUserList:function(){var e=this;this.UserName.length>0?this.userParams.UserName=this.UserName:delete this.userParams.UserName,Object(s.d)(this.userParams).then(function(t){t.data.data.users.forEach(function(e){e.Role={1:"管理员",4:"普通用户"}[e.RoleID]}),e.userData=t.data.data.users,e.userPagination.total=t.data.data.total})},handleConfirmDelete:function(e){this.selectedRow=e,this.isDelete=!0},handleDelete:function(){var e=this;Object(s.c)(this.selectedRow.UserName).then(function(t){"00000000"===t.data.status?(e.$message({message:e.$t("SUCCESS_DELETE")}),e.isDelete=!1,e.fetchUserList()):"21000001"===t.data.status?(e.$message({message:e.$t("ERR_DELETE")+"。"+e.$t("ERR_CONNECT_AIVAULT")}),e.isDelete=!1):(e.$message({message:e.$t("ERR_DELETE")+"。"+e.$t("ERR_DELETE_USER")}),e.isDelete=!1)}).catch(function(t){e.isDelete=!1})},handleConfirmAddUser:function(){this.isAddUser=!0},handleCancel:function(){this.isAddUser=!1,this.fetchUserList()},handleSizeChange:function(e){this.userParams.PageSize=e,this.fetchUserList()},handleCurrentChange:function(e){this.userParams.CurrentPage=e,this.fetchUserList()},handleClear:function(){this.fetchUserList()}}},r={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticStyle:{"margin-bottom":"20px"}},[a("div",{staticClass:"user-operation"},[a("el-button",{attrs:{type:"primary",plain:""},on:{click:e.handleConfirmAddUser}},[e._v("\n              "+e._s(e.$t("BUTTON_ADD_USER"))+"\n        ")]),e._v(" "),a("el-input",{staticClass:"input-search",attrs:{type:"text","prefix-icon":"el-icon-search",placeholder:e.$t("PLACEHOLDER_INPUT"),clearable:""},on:{clear:e.handleClear},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.fetchUserList.apply(null,arguments)}},model:{value:e.UserName,callback:function(t){e.UserName=t},expression:"UserName"}}),e._v(" "),a("el-button",{staticClass:"button-refresh",attrs:{icon:"el-icon-refresh"},on:{click:e.fetchUserList}})],1),e._v(" "),a("el-table",{staticStyle:{width:"100%","margin-top":"40px","margin-bottom":"20px"},attrs:{data:e.userData,"cell-style":{textAlign:"center",border:"0.5px solid rgb(123, 143, 175, 0.5)",padding:"10px 0"},"header-cell-style":{textAlign:"center",padding:"10px 0"},"empty-text":e.$t("EMPTY_TEXT")}},[a("el-table-column",{attrs:{prop:"UserID",label:e.$t("COLUMN_USER_ID")}}),e._v(" "),a("el-table-column",{attrs:{prop:"UserName",label:e.$t("COLUMN_USER_NAME")}}),e._v(" "),a("el-table-column",{attrs:{prop:"Role",label:e.$t("COLUMN_USER_TYPE")}}),e._v(" "),a("el-table-column",{attrs:{prop:"CreateTime",label:e.$t("COLUMN_CREATE_TIME")}}),e._v(" "),a("el-table-column",{attrs:{prop:"operation",label:e.$t("COLUMN_OPERATION"),width:"120"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{attrs:{type:"danger",disabled:1===t.row.RoleID,plain:"",size:"small"},on:{click:function(a){return e.handleConfirmDelete(t.row)}}},[e._v("\n                    "+e._s(e.$t("OPERATION_DELETE"))+"\n                ")])]}}])})],1),e._v(" "),a("el-pagination",{staticStyle:{"padding-bottom":"30px"},attrs:{total:e.userPagination.total,"page-size":e.userParams.PageSize,layout:"prev, pager, next"},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}}),e._v(" "),a("el-dialog",{attrs:{title:e.$t("CONFIRM_DELETE"),visible:e.isDelete,width:"28%","close-on-click-modal":!1,modal:!1},on:{"update:visible":function(t){e.isDelete=t}}},[e._v("\n        "+e._s(e.$t("CONFIRM_DELETE_TIP"))+" "+e._s(e.selectedRow.UserName)+"?\n        "),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){e.isDelete=!1}}},[e._v(e._s(e.$t("BTN_CANCEL")))]),e._v(" "),a("el-button",{attrs:{type:"primary"},on:{click:e.handleDelete}},[e._v(e._s(e.$t("BTN_OK")))])],1)]),e._v(" "),a("user-manage",{attrs:{isShow:e.isAddUser,currOperation:"addUser"},on:{handleCancel:e.handleCancel}})],1)},staticRenderFns:[]};var l=a("VU/8")(n,r,!1,function(e){a("z0N8")},"data-v-b440db6e",null);t.default=l.exports},z0N8:function(e,t){}});
//# sourceMappingURL=2.f2e440dc37d93b7b59a1.js.map
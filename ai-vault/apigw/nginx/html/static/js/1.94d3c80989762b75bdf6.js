webpackJsonp([1],{"7d5q":function(t,e){},HXef:function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=r("Xxa5"),n=r.n(i),a=r("exGp"),o=r.n(a),s=r("Dd8w"),l=r.n(s),c=r("lta2");function u(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};arguments.length>1&&void 0!==arguments[1]&&arguments[1];return Object(c.b)("/datamanager/v1/export",l()({},t),{responseType:"blob",signal:!1})}var h=r("y5xs"),d={name:"home",data:function(){return{useramount:0,datasize:0,version:"***",tableData:[],isAhealth:!1,isUhealth:!1,isDhealth:!1,tmpVersion:"",tmpTableData:[],tmpHealthStatus:!1,isQueryVersion:!1,isQueryCert:!1,isQueryHealth:!1,fileList:[],isConfirmUploading:!1,isUploading:!1,isDownloading:!1,mgmtcert:{CertType:"管理面",CertValidDate:"***",CertAlarm:"***",CrlStatus:"***"},svccert:{CertType:"服务面",CertValidDate:"***",CertAlarm:"***",CrlStatus:"***"},abortController:new AbortController}},mounted:function(){this.fetchData()},methods:{handleGetUserAmount:function(){var t=this;Object(h.d)({},{signal:this.abortController.signal}).then(function(e){"00000000"===e.data.status?(t.useramount=e.data.data.total,t.isUhealth=!0):(t.useramount=0,t.isUhealth=!1)})},handleGetDataSize:function(){var t=this;(function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{};return Object(c.b)("/datamanager/v1/size",t,e)})({},{signal:this.abortController.signal}).then(function(e){"00000000"===e.data.status?(t.datasize=(e.data.data.size/1024/1024).toFixed(2),t.isDhealth=!0):(t.datasize=0,t.isDhealth=!1)})},queryVersion:function(){var t=this;(function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{};return Object(c.b)("/AIVAULT/v1/version/",t,e)})({},{signal:this.abortController.signal}).then(function(e){t.tmpVersion=e.data.data.version.split("_")[0],t.isQueryVersion=!0})},queryHealth:function(){var t=this;(function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{};return Object(c.b)("/AIVAULT/v1/health",t,e)})({},{signal:this.abortController.signal}).then(function(e){t.tmpHealthStatus=e.data.msg,t.isQueryHealth=!0})},queryCert:function(){var t=this;(function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{};return Object(c.b)("/AIVAULT/v1/certStatus",t,e)})({},{signal:this.abortController.signal}).then(function(e){t.tmpTableData=e.data.data,t.isQueryCert=!0})},fetchData:function(){this.handleGetUserAmount(),this.handleGetDataSize(),this.queryVersion(),this.queryHealth(),this.queryCert()},handleSpan:function(){var t=this,e=this.tableData.filter(function(t){return"MGMT"===t.CertType}),r=this.tableData.filter(function(t){return"MGMT"!==t.CertType});this.tableData=e.concat(r),this.tableData.forEach(function(e,r){"MGMT"===e.CertType&&(t.mgmtcert.CertAlarm=""===e.CertAlarm?"正常":"不正常",t.mgmtcert.CrlStatus="No CRL certificate has been imported."===e.CrlStatus?"未导入":"已导入",t.mgmtcert.CertValidDate=e.CertValidDate),t.svccert.CertAlarm=""===e.CertAlarm?"正常":"不正常",t.svccert.CrlStatus="No CRL certificate has been imported."===e.CrlStatus?"未导入":"已导入",t.svccert.CertValidDate=e.CertValidDate})},handleBeforeUpload:function(t){this.isUploading=!0;var e=t.type.indexOf("zip")>-1,r=t.size/1024/1024<=50;return e||(this.$message.error(this.$t("ERR_UPLOAD_FILE_TYPE")),this.isUploading=!1),r||(this.$message.error(this.$t("ERR_UPLOAD_FILE_SIZE")),this.isUploading=!1),e&&r},handleDownload:function(){var t=this;return o()(n.a.mark(function e(){var r,i,a,o,s;return n.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return t.isDownloading=!0,e.next=3,u();case 3:r=e.sent,i=new Blob([r.data],{type:"application/zip"}),a=r.headers["content-disposition"].split(";")[1].split("=")[1],window.navigator&&window.navigator.msSaveOrOpenBlob?(window.navigator.msSaveBlob(i,a),console.log(1)):(o=window.URL||window.webkitURL||window.moxURL,(s=document.createElement("a")).href=o.createObjectURL(i),s.download=a,document.body.appendChild(s),s.click(),document.body.removeChild(s),window.URL.revokeObjectURL(o)),t.isDownloading=!1;case 8:case"end":return e.stop()}},e,t)}))()},handleUploadSuccess:function(t,e,r){"00000000"===t.status?this.$message.success({message:this.$t("SUCCESS_UPLOAD")}):this.$message.warning({message:this.$t("ERR_UPLOAD")}),this.handleGetUserAmount(),this.isUploading=!1},handleUploadError:function(t,e,r){this.$message.warning({message:this.$t("ERR_UPLOAD")}),this.isUploading=!1}}},v={render:function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"home"},[i("div",{staticClass:"left"},[i("div",{staticClass:"left-box first-left"},[i("div",{staticClass:"left-name"},[t._v(t._s(t.$t("USER_AMOUNT")))]),t._v(" "),i("div",{staticClass:"left-num"},[t._v(t._s(t.useramount))])]),t._v(" "),i("div",{staticClass:"left-box"},[i("div",{staticClass:"left-name"},[t._v(t._s(t.$t("SYS_DATA_SIZE")))]),t._v(" "),i("div",{staticClass:"left-num"},[t._v(t._s(t.datasize))])])]),t._v(" "),i("div",{staticClass:"right"},[i("div",{staticClass:"right-box right-top"},[i("div",[i("div",{staticClass:"title"},[t._v(t._s(t.$t("TOOL_INFO")))])]),t._v(" "),i("div",{staticClass:"top-button"},[i("el-button",{directives:[{name:"no-more-click",rawName:"v-no-more-click"}],staticStyle:{color:"#D3DCE9"},attrs:{type:"text",icon:"el-icon-upload2",loading:t.isUploading},on:{click:function(e){t.isConfirmUploading=!0}}},[t._v(t._s(t.$t("BUTTON_UPLOAD"))+"\n        ")]),t._v(" "),i("el-button",{directives:[{name:"no-more-click",rawName:"v-no-more-click"}],staticStyle:{color:"#D3DCE9"},attrs:{type:"text",icon:"el-icon-download",loading:t.isDownloading},on:{click:t.handleDownload}},[t._v(t._s(t.$t("BUTTON_DOWNLOAD"))+"\n        ")])],1),t._v(" "),i("div",{staticClass:"info-block"},[i("div",{staticClass:"right_name"},[t._v(t._s(t.$t("VERSION")))]),t._v(" "),i("div",{staticClass:"right_info"},[t._v(t._s(t.version))])]),t._v(" "),i("div",{staticClass:"info-block"},[i("div",{staticClass:"right_name"},[t._v(t._s(t.$t("HEALTH_STATUS")))]),t._v(" "),i("div",{staticClass:"health_info",staticStyle:{"margin-top":"5px"}},[this.isAhealth?i("div",{staticStyle:{display:"flex","flex-direction":"row"}},[i("img",{staticStyle:{margin:"8px"},attrs:{src:r("nwfx")}}),t._v(" "),i("div",{staticStyle:{"font-size":"20px","line-height":"30px","font-weight":"400","letter-spacing":"0",color:"#FFFFFE",margin:"8px"}},[t._v("\n              健康\n            ")])]):i("div",{staticStyle:{display:"flex","flex-direction":"row"}},[i("img",{staticStyle:{margin:"8px"},attrs:{src:r("vigF")}}),t._v(" "),i("div",{staticStyle:{"font-size":"20px","line-height":"30px","font-weight":"400","letter-spacing":"0",color:"#FFFFFE",margin:"0 8px"}},[t._v("\n              不健康\n            ")])])])])]),t._v(" "),i("div",{staticClass:"right-box"},[i("div",{staticClass:"title"},[t._v(t._s(t.$t("CERT_INFO")))]),t._v(" "),i("div",{staticClass:"info-block"},[i("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_TYPE")))]),t._v(" "),i("div",{staticClass:"right_info"},[t._v(t._s(t.mgmtcert.CertType))])]),t._v(" "),i("div",{staticClass:"info-block"},[i("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_VALID_DATE")))]),t._v(" "),i("div",{staticClass:"right_info"},[t._v(t._s(t.mgmtcert.CertValidDate))])]),t._v(" "),i("div",{staticClass:"info-block"},[i("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_ALARM")))]),t._v(" "),i("div",{staticClass:"right_info"},[t._v(t._s(t.mgmtcert.CertAlarm))])]),t._v(" "),i("div",{staticClass:"info-block"},[i("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CRL_STATUS")))]),t._v(" "),i("div",{staticClass:"right_info"},[t._v(t._s(t.mgmtcert.CrlStatus))])])]),t._v(" "),i("div",{staticClass:"right-box"},[i("div",{staticClass:"title"},[t._v(t._s(t.$t("CERT_INFO")))]),t._v(" "),i("div",{staticClass:"info-block"},[i("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_TYPE")))]),t._v(" "),i("div",{staticClass:"right_info"},[t._v(t._s(t.svccert.CertType))])]),t._v(" "),i("div",{staticClass:"info-block"},[i("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_VALID_DATE")))]),t._v(" "),i("div",{staticClass:"right_info"},[t._v(t._s(t.svccert.CertValidDate))])]),t._v(" "),i("div",{staticClass:"info-block"},[i("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_ALARM")))]),t._v(" "),i("div",{staticClass:"right_info"},[t._v(t._s(t.svccert.CertAlarm))])]),t._v(" "),i("div",{staticClass:"info-block"},[i("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CRL_STATUS")))]),t._v(" "),i("div",{staticClass:"right_info"},[t._v(t._s(t.svccert.CrlStatus))])])])]),t._v(" "),i("el-dialog",{attrs:{title:t.$t("UPLOAD_RISK"),visible:t.isConfirmUploading,width:"28%","close-on-click-modal":!1,modal:!1},on:{"update:visible":function(e){t.isConfirmUploading=e}}},[i("div",{staticClass:"dialog-tip"},[i("div",{staticStyle:{"margin-left":"16px","margin-right":"16px"}},[i("img",{attrs:{src:r("77VW")}})]),t._v("\n      "+t._s(t.$t("CONFIRM_UPLOAD_TIP"))+"\n    ")]),t._v(" "),i("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{directives:[{name:"no-more-click",rawName:"v-no-more-click"}],staticClass:"dialog-button",on:{click:function(e){t.isConfirmUploading=!1}}},[t._v(t._s(t.$t("BTN_CANCEL")))]),t._v(" "),i("el-upload",{staticClass:"upload-demo",staticStyle:{display:"inline-block"},attrs:{action:"/datamanager/v1/import","file-list":t.fileList,"before-upload":t.handleBeforeUpload,"show-file-list":!1,"on-success":t.handleUploadSuccess,"on-error":t.handleUploadError}},[i("el-button",{directives:[{name:"no-more-click",rawName:"v-no-more-click"}],staticClass:"dialog-button",attrs:{type:"primary"},on:{click:function(e){t.isConfirmUploading=!1}}},[t._v(t._s(t.$t("BUTTON_UPLOAD")))])],1)],1)])],1)},staticRenderFns:[]};var f=r("VU/8")(d,v,!1,function(t){r("7d5q")},"data-v-4b330089",null);e.default=f.exports},SldL:function(t,e){!function(e){"use strict";var r,i=Object.prototype,n=i.hasOwnProperty,a="function"==typeof Symbol?Symbol:{},o=a.iterator||"@@iterator",s=a.asyncIterator||"@@asyncIterator",l=a.toStringTag||"@@toStringTag",c="object"==typeof t,u=e.regeneratorRuntime;if(u)c&&(t.exports=u);else{(u=e.regeneratorRuntime=c?t.exports:{}).wrap=C;var h="suspendedStart",d="suspendedYield",v="executing",f="completed",p={},_={};_[o]=function(){return this};var g=Object.getPrototypeOf,m=g&&g(g(A([])));m&&m!==i&&n.call(m,o)&&(_=m);var y=x.prototype=b.prototype=Object.create(_);L.prototype=y.constructor=x,x.constructor=L,x[l]=L.displayName="GeneratorFunction",u.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===L||"GeneratorFunction"===(e.displayName||e.name))},u.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,x):(t.__proto__=x,l in t||(t[l]="GeneratorFunction")),t.prototype=Object.create(y),t},u.awrap=function(t){return{__await:t}},U(E.prototype),E.prototype[s]=function(){return this},u.AsyncIterator=E,u.async=function(t,e,r,i){var n=new E(C(t,e,r,i));return u.isGeneratorFunction(e)?n:n.next().then(function(t){return t.done?t.value:n.next()})},U(y),y[l]="Generator",y[o]=function(){return this},y.toString=function(){return"[object Generator]"},u.keys=function(t){var e=[];for(var r in t)e.push(r);return e.reverse(),function r(){for(;e.length;){var i=e.pop();if(i in t)return r.value=i,r.done=!1,r}return r.done=!0,r}},u.values=A,D.prototype={constructor:D,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=r,this.done=!1,this.delegate=null,this.method="next",this.arg=r,this.tryEntries.forEach(T),!t)for(var e in this)"t"===e.charAt(0)&&n.call(this,e)&&!isNaN(+e.slice(1))&&(this[e]=r)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var e=this;function i(i,n){return s.type="throw",s.arg=t,e.next=i,n&&(e.method="next",e.arg=r),!!n}for(var a=this.tryEntries.length-1;a>=0;--a){var o=this.tryEntries[a],s=o.completion;if("root"===o.tryLoc)return i("end");if(o.tryLoc<=this.prev){var l=n.call(o,"catchLoc"),c=n.call(o,"finallyLoc");if(l&&c){if(this.prev<o.catchLoc)return i(o.catchLoc,!0);if(this.prev<o.finallyLoc)return i(o.finallyLoc)}else if(l){if(this.prev<o.catchLoc)return i(o.catchLoc,!0)}else{if(!c)throw new Error("try statement without catch or finally");if(this.prev<o.finallyLoc)return i(o.finallyLoc)}}}},abrupt:function(t,e){for(var r=this.tryEntries.length-1;r>=0;--r){var i=this.tryEntries[r];if(i.tryLoc<=this.prev&&n.call(i,"finallyLoc")&&this.prev<i.finallyLoc){var a=i;break}}a&&("break"===t||"continue"===t)&&a.tryLoc<=e&&e<=a.finallyLoc&&(a=null);var o=a?a.completion:{};return o.type=t,o.arg=e,a?(this.method="next",this.next=a.finallyLoc,p):this.complete(o)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),p},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.finallyLoc===t)return this.complete(r.completion,r.afterLoc),T(r),p}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.tryLoc===t){var i=r.completion;if("throw"===i.type){var n=i.arg;T(r)}return n}}throw new Error("illegal catch attempt")},delegateYield:function(t,e,i){return this.delegate={iterator:A(t),resultName:e,nextLoc:i},"next"===this.method&&(this.arg=r),p}}}function C(t,e,r,i){var n=e&&e.prototype instanceof b?e:b,a=Object.create(n.prototype),o=new D(i||[]);return a._invoke=function(t,e,r){var i=h;return function(n,a){if(i===v)throw new Error("Generator is already running");if(i===f){if("throw"===n)throw a;return R()}for(r.method=n,r.arg=a;;){var o=r.delegate;if(o){var s=O(o,r);if(s){if(s===p)continue;return s}}if("next"===r.method)r.sent=r._sent=r.arg;else if("throw"===r.method){if(i===h)throw i=f,r.arg;r.dispatchException(r.arg)}else"return"===r.method&&r.abrupt("return",r.arg);i=v;var l=w(t,e,r);if("normal"===l.type){if(i=r.done?f:d,l.arg===p)continue;return{value:l.arg,done:r.done}}"throw"===l.type&&(i=f,r.method="throw",r.arg=l.arg)}}}(t,r,o),a}function w(t,e,r){try{return{type:"normal",arg:t.call(e,r)}}catch(t){return{type:"throw",arg:t}}}function b(){}function L(){}function x(){}function U(t){["next","throw","return"].forEach(function(e){t[e]=function(t){return this._invoke(e,t)}})}function E(t){var e;this._invoke=function(r,i){function a(){return new Promise(function(e,a){!function e(r,i,a,o){var s=w(t[r],t,i);if("throw"!==s.type){var l=s.arg,c=l.value;return c&&"object"==typeof c&&n.call(c,"__await")?Promise.resolve(c.__await).then(function(t){e("next",t,a,o)},function(t){e("throw",t,a,o)}):Promise.resolve(c).then(function(t){l.value=t,a(l)},o)}o(s.arg)}(r,i,e,a)})}return e=e?e.then(a,a):a()}}function O(t,e){var i=t.iterator[e.method];if(i===r){if(e.delegate=null,"throw"===e.method){if(t.iterator.return&&(e.method="return",e.arg=r,O(t,e),"throw"===e.method))return p;e.method="throw",e.arg=new TypeError("The iterator does not provide a 'throw' method")}return p}var n=w(i,t.iterator,e.arg);if("throw"===n.type)return e.method="throw",e.arg=n.arg,e.delegate=null,p;var a=n.arg;return a?a.done?(e[t.resultName]=a.value,e.next=t.nextLoc,"return"!==e.method&&(e.method="next",e.arg=r),e.delegate=null,p):a:(e.method="throw",e.arg=new TypeError("iterator result is not an object"),e.delegate=null,p)}function S(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function T(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function D(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(S,this),this.reset(!0)}function A(t){if(t){var e=t[o];if(e)return e.call(t);if("function"==typeof t.next)return t;if(!isNaN(t.length)){var i=-1,a=function e(){for(;++i<t.length;)if(n.call(t,i))return e.value=t[i],e.done=!1,e;return e.value=r,e.done=!0,e};return a.next=a}}return{next:R}}function R(){return{value:r,done:!0}}}(function(){return this}()||Function("return this")())},Xxa5:function(t,e,r){t.exports=r("jyFz")},exGp:function(t,e,r){"use strict";e.__esModule=!0;var i,n=r("//Fk"),a=(i=n)&&i.__esModule?i:{default:i};e.default=function(t){return function(){var e=t.apply(this,arguments);return new a.default(function(t,r){return function i(n,o){try{var s=e[n](o),l=s.value}catch(t){return void r(t)}if(!s.done)return a.default.resolve(l).then(function(t){i("next",t)},function(t){i("throw",t)});t(l)}("next")})}}},jyFz:function(t,e,r){var i=function(){return this}()||Function("return this")(),n=i.regeneratorRuntime&&Object.getOwnPropertyNames(i).indexOf("regeneratorRuntime")>=0,a=n&&i.regeneratorRuntime;if(i.regeneratorRuntime=void 0,t.exports=r("SldL"),n)i.regeneratorRuntime=a;else try{delete i.regeneratorRuntime}catch(t){i.regeneratorRuntime=void 0}}});
//# sourceMappingURL=1.94d3c80989762b75bdf6.js.map